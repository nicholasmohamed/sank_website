import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import SankMerchDb as SankMerchDbModel


class Merchandise(SQLAlchemyObjectType):
    class Meta:
        model = SankMerchDbModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_merchandise = SQLAlchemyConnectionField(Merchandise.connection)


schema = graphene.Schema(query=Query)