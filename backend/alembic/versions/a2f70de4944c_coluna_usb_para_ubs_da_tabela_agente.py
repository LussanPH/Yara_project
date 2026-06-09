"""Coluna Usb para Ubs da Tabela Agente

Revision ID: a2f70de4944c
Revises: f4a7ba21a476
Create Date: 2026-06-09 10:50:54.262241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2f70de4944c'
down_revision: Union[str, Sequence[str], None] = 'f4a7ba21a476'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('Agentes') as batch_op:
        batch_op.alter_column(
            column_name='usb_atuante',    
            new_column_name='ubs_atuante' 
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('Agentes') as batch_op:
        batch_op.alter_column(
            column_name='ubs_atuante',
            new_column_name='usb_atuante'
        )
