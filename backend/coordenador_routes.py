from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import create_session, somente_CM, get_usuario
from security import get_hashed_password
from fastapi.responses import Response
from models import Notificacao, Coordenador_Municipal
from schemas import CMSchema
from fastapi.responses import StreamingResponse
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

cm_router = APIRouter(prefix="/cm", tags=["cm"], dependencies=[Depends(somente_CM)])


#Criaçaõ de conta CM
@cm_router.post("/criar_conta")
async def criar_cm(cm_schema : CMSchema, session : Session = Depends(create_session)): 
    cm = session.query(Coordenador_Municipal).filter(Coordenador_Municipal.email == cm_schema.email).first()

    if cm:
        raise HTTPException(status_code=400, detail="UBS já cadastrada no sistema!")
    
    senha_hashed = get_hashed_password(cm_schema.senha)
    cm_novo = Coordenador_Municipal(cm_schema.email, senha_hashed, cm_schema.nome, cm_schema.municipio)
    session.add(cm_novo)
    session.commit()
    
    return {"message": "Coordenador Municipal criado com sucesso!"}


#Lista notificações da região
@cm_router.get("/listar_notificacoes")
async def listar_notificacoes_ubs(usuario = Depends(get_usuario), session : Session = Depends(create_session)):
    try:
        notificacoes = session.query(Notificacao).filter(Notificacao.municipio == usuario.municipio, Notificacao.validado == True).all()      #RETORNA TODAS AS NOTIFICAÇÕOS DA REGIÃO QUE FORAM VALIDADAS

        return {"notificacoes": notificacoes, "quantidade": len(notificacoes)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar notificações: {str(e)}")


#Alteração dos status de uma notificação
@cm_router.patch("/notificacoes/{notificacao_id}/status_recebido")
async def validar_notificacao(notificacao_id: int, usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).filter(Notificacao.id == notificacao_id, Notificacao.municipio == usuario.municipio, Notificacao.validado == True).first()

    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")

    notificacao.status = "RECEBIDO"
    session.commit()

    return {"message":"Notificação recebida!"}


@cm_router.patch("/notificacoes/{notificacao_id}/status_em_investigacao")
async def validar_notificacao(notificacao_id: int, usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).filter(Notificacao.id == notificacao_id, Notificacao.municipio == usuario.municipio, Notificacao.validado == True).first()

    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")

    notificacao.status = "EM INVESTIGAÇÃO"
    session.commit()

    return {"message":"Notificação em investigação!"}


@cm_router.patch("/notificacoes/{notificacao_id}/status_confirmado")
async def validar_notificacao(notificacao_id: int, usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).filter(Notificacao.id == notificacao_id, Notificacao.municipio == usuario.municipio, Notificacao.validado == True).first()

    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")

    notificacao.status = "CONFIRMADO"
    session.commit()

    return {"message":"Notificação confirmada!"}


@cm_router.patch("/notificacoes/{notificacao_id}/status_descartado")
async def validar_notificacao(notificacao_id: int, usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).filter(Notificacao.id == notificacao_id, Notificacao.municipio == usuario.municipio, Notificacao.validado == True).first()

    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")

    notificacao.status = "DESCARTADO"
    session.commit()

    return {"message":"Notificação descartada!"}


@cm_router.patch("/notificacoes/{notificacao_id}/status_encerrado")
async def validar_notificacao(notificacao_id: int, usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).filter(Notificacao.id == notificacao_id, Notificacao.municipio == usuario.municipio, Notificacao.validado == True).first()

    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")

    notificacao.status = "ENCERRADO"
    session.commit()

    return {"message":"Notificação encerrada!"}

# Adicionar em cm_router.py

# Métricas resumidas do município
@cm_router.get("/dashboard_stats")
async def obter_estatisticas(usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    try:
        total = session.query(Notificacao).filter(Notificacao.municipio == usuario.municipio, Notificacao.validado == True).count()
        investigacao = session.query(Notificacao).filter(Notificacao.municipio == usuario.municipio, Notificacao.validado == True, Notificacao.status == "EM INVESTIGAÇÃO").count()
        confirmados = session.query(Notificacao).filter(Notificacao.municipio == usuario.municipio, Notificacao.validado == True, Notificacao.status == "CONFIRMADO").count()
        
        return {
            "total": total,
            "em_investigacao": investigacao,
            "confirmados": confirmados
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar estatísticas: {str(e)}")

@cm_router.get("/exportar_relatorio")
async def exportar_relatorio(usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    try:
        notificacoes = session.query(Notificacao).filter(
            Notificacao.municipio == usuario.municipio, 
            Notificacao.validado == True
        ).all()
        
        relatorio = [
            {
                "id": n.id,
                "categoria": getattr(n, 'categoria', 'N/A'),
                "tipo": getattr(n, 'tipo', 'N/A'),
                "status": n.status,
                "data": getattr(n, 'data_criacao', 'N/A'),
                "local": getattr(n, 'local', 'N/A')
            }
            for n in notificacoes
        ]
        
        return {"relatorio": relatorio, "municipio": usuario.municipio}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatório: {str(e)}")

@cm_router.get("/exportar_relatorio/pdf")
async def exportar_relatorio_pdf(
    usuario=Depends(get_usuario),
    session: Session = Depends(create_session)
):
    try:
        notificacoes = (
            session.query(Notificacao)
            .filter(
                Notificacao.municipio == usuario.municipio,
                Notificacao.validado == True
            )
            .order_by(Notificacao.data_envio.desc())
            .all()
        )

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        styles = getSampleStyleSheet()
        elementos = []

        titulo = styles["Title"]
        titulo.alignment = TA_CENTER

        elementos.append(
            Paragraph(
                "Relatório de Notificações",
                titulo
            )
        )

        elementos.append(Spacer(1, 12))

        elementos.append(
            Paragraph(
                f"Município: {usuario.municipio}",
                styles["Normal"]
            )
        )

        elementos.append(
            Paragraph(
                f"Total de notificações: {len(notificacoes)}",
                styles["Normal"]
            )
        )

        elementos.append(Spacer(1, 20))

        dados = [[
            "ID",
            "Categoria",
            "Evento",
            "Status",
            "Local",
            "Data"
        ]]

        for n in notificacoes:
            dados.append([
                str(n.id),
                str(n.categoria or "-"),
                str(n.tipo_evento or "-"),
                str(n.status or "-"),
                str(n.local_ocorrencia or "-"),
                (
                    n.data_envio.strftime("%d/%m/%Y %H:%M")
                    if n.data_envio
                    else "-"
                ),
            ])

        tabela = Table(
            dados,
            repeatRows=1,
            colWidths=[35, 65, 90, 80, 100, 75],
        )

        tabela.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#0F6E56")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F5F8F7")
                    ]
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
            ])
        )

        elementos.append(tabela)

        doc.build(elementos)

        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    f'attachment; filename="relatorio_{usuario.municipio}.pdf"'
                )
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar PDF: {str(e)}"
        )
        
@cm_router.get("/notificacoes/{notificacao_id}/relatorio_pdf")
async def gerar_relatorio_notificacao_pdf(
    notificacao_id: int,
    usuario=Depends(get_usuario),
    session: Session = Depends(create_session)
):
    try:
        notificacao = session.query(Notificacao).filter(
            Notificacao.id == notificacao_id,
            Notificacao.municipio == usuario.municipio,
            Notificacao.validado == True
        ).first()

        if not notificacao:
            raise HTTPException(
                status_code=404,
                detail="Notificação não encontrada."
            )

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()

        titulo = styles["Title"]
        titulo.alignment = TA_CENTER

        elementos = []

        elementos.append(
            Paragraph(
                "Relatório da Notificação",
                titulo
            )
        )

        elementos.append(Spacer(1, 20))

        dados = [
            ["Protocolo", f"#{str(notificacao.id).zfill(7)}"],
            ["Município", str(notificacao.municipio or "—")],
            ["Tipo do evento", str(notificacao.tipo_evento or "—")],
            ["Categoria", str(notificacao.categoria or "—")],
            ["Status", str(notificacao.status or "—")],
            ["Data de envio", str(notificacao.data_envio or "—")],
            ["Local", str(notificacao.local_ocorrencia or "—")],
            [
                "Afetados",
                str(
                    notificacao.pessoas_animais_infectados_afetados
                    or 0
                )
            ],
            [
                "Continuidade da situação",
                str(notificacao.continuidade_situacao or "—")
            ],
        ]

        tabela = Table(
            dados,
            colWidths=[160, 320]
        )

        tabela.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("PADDING", (0, 0), (-1, -1), 8),
            ])
        )

        elementos.append(tabela)

        elementos.append(Spacer(1, 20))

        elementos.append(
            Paragraph(
                "<b>Descrição</b>",
                styles["Heading2"]
            )
        )

        elementos.append(Spacer(1, 8))

        descricao = (
            notificacao.descricao
            or "Nenhuma descrição informada."
        )

        # Quebra linhas da descrição
        descricao = descricao.replace("\n", "<br/>")

        elementos.append(
            Paragraph(
                descricao,
                styles["BodyText"]
            )
        )

        doc.build(elementos)

        pdf_bytes = buffer.getvalue()
        buffer.close()

        nome_arquivo = (
            f"notificacao_{notificacao.id}_"
            f"{notificacao.municipio}.pdf"
        )

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    f'attachment; filename="{nome_arquivo}"'
                )
            }
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar relatório: {str(e)}"
        )