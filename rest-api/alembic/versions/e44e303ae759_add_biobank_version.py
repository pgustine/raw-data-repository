"""add biobank version

Revision ID: e44e303ae759
Revises: 0e92151ebd4a
Create Date: 2018-08-20 10:08:20.904521

"""
from alembic import op
import sqlalchemy as sa
import model.utils


from participant_enums import PhysicalMeasurementsStatus, QuestionnaireStatus, OrderStatus
from participant_enums import WithdrawalStatus, SuspensionStatus, QuestionnaireDefinitionStatus
from participant_enums import EnrollmentStatus, Race, SampleStatus, OrganizationType, BiobankOrderStatus
from participant_enums import MetricSetType, MetricsKey
from model.site_enums import SiteStatus, EnrollingStatus, DigitalSchedulingStatus, ObsoleteStatus
from model.code import CodeType

# revision identifiers, used by Alembic.
revision = 'e44e303ae759'
down_revision = '0e92151ebd4a'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()



def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('biobank_order', sa.Column('version', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('biobank_order', 'version')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

