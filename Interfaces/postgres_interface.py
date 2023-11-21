import logging
from typing import Any
import uuid
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import String, Boolean, Uuid, Double, DateTime, ForeignKey, create_engine, Column, PrimaryKeyConstraint

class Base(DeclarativeBase):
    pass
class Stadium(Base):
    __tablename__       = 'stadiums'

    stadium_id          = Column('stadium_id', Uuid, primary_key=True)
    stadium_name        = Column('stadium_name', String)

    def __init__(self, stadium_name):
        self.stadium_id     = uuid.uuid4()
        self.stadium_name   = stadium_name

    def __repr__(self) -> str:
        return f'{self.stadium_id} ({self.stadium_name})'
    
class Team(Base):
    __tablename__       = 'teams'
    
    team_id             = Column('team_id', Uuid, primary_key=True)
    team_name           = Column('team_name', String)
    stadium_id          = Column(Uuid, ForeignKey('stadiums.stadium_id'))
    primary_color       = Column('primary_color', String)
    secondary_color     = Column('secondary_color', String)
    tertiary_color      = Column('tertiary_color', String)
    primary_team_logo   = Column('primary_team_logo', String)
    secondary_team_logo = Column('secondary_team_logo', String)
    tertiary_team_logo  = Column('tertiary_team_logo', String)

    def __init__(self, stadium_id, team_name,
                 primary_color=None, secondary_color=None, tertiary_color=None,
                 primary_team_logo=None, secondary_team_logo=None, tertiary_team_logo=None):
        self.team_id                = uuid.uuid4()
        self.team_name              = team_name
        self.stadium_id             = stadium_id
        self.primary_color          = primary_color
        self.secondary_color        = secondary_color
        self.tertiary_color         = tertiary_color
        self.primary_team_logo      = primary_team_logo
        self.secondary_team_logo    = secondary_team_logo
        self.tertiary_team_logo     = tertiary_team_logo

    def __repr__(self) -> str:
        return f'{self.team_id} ({self.stadium_id}) ({self.primary_color})'  

class Vendor(Base):
    __tablename__       = 'vendors'

    vendor_id           = Column('vendor_id', Uuid, primary_key=True)
    vendor_name         = Column('vendor_name', String)
    stadium_id          = Column(ForeignKey('stadiums.stadium_id'))
    team_id             = Column(ForeignKey('teams.team_id'))

    def __init__(self, vendor_name, stadium_id, team_id=None):
        self.vendor_id      = uuid.uuid4()
        self.vendor_name    = vendor_name
        self.stadium_id     = stadium_id
        self.team_id        = team_id

    def __repr__(self) -> str:
        return f'{self.vendor_id} ({self.vendor_name}) ({self.stadium_id}) ({self.team_id})'

class Product(Base):
    __tablename__       = 'products'

    product_id          = Column('product_id', Uuid, primary_key=True)
    product_name        = Column('product_name', String)
    product_cost        = Column('product_cost', Double)

    def __init__(self, product_name, product_cost):
        self.product_id     = uuid.uuid4()
        self.product_name   = product_name
        self.product_cost   = product_cost

    def __repr__(self) -> str:
        return f'{self.product_id} ({self.product_name}) ({self.product_cost})'
    
class MenuOption(Base):
    __tablename__       = 'menu_options'

    vendor_id           = Column(Uuid, ForeignKey('vendors.vendor_id'), primary_key=True)
    product_id          = Column(Uuid, ForeignKey('products.product_id'), primary_key=True)

    __table_args__ = (
        PrimaryKeyConstraint('vendor_id', 'product_id'),
    )

    def __init__(self, vendor_id, product_id):
        self.vendor_id  = vendor_id
        self.product_id = product_id

    def __repr__(self) -> str:
        return f'({self.vendor_id}) ({self.product_id})'
    
class Session(Base):
    __tablename__       = 'sessions'

    session_id          = Column('session_id', Uuid, primary_key=True)
    session_date        = Column('session_date', DateTime)
    session_name        = Column('session_name', String)
    team_id             = Column(Uuid, ForeignKey('teams.team_id'))
    active              = Column('active', Boolean)

    def __init__(self, session_date, session_name, team_id, active):
        self.session_id     = uuid.uuid4()
        self.session_date   = session_date
        self.session_name   = session_name
        self.team_id        = team_id
        self.active         = active

    def __repr__(self) -> str:
        return f'{self.session_id} ({self.session_date}) ({self.session_name}) ({self.team_id}) ({self.active})'

class Transaction(Base):
    __tablename__       = 'transactions'

    transaction_id      = Column('transaction_id', Uuid, primary_key=True)
    order_id            = Column('order_id', Uuid)
    date_time           = Column('date_time', DateTime)
    product_id          = Column(Uuid, ForeignKey('products.product_id'))
    session_id          = Column(Uuid, ForeignKey('sessions.session_id'))

    def __init__(self, order_id, product_id, session_id):
        self.transaction_id     = uuid.uuid4()
        self.order_id           = order_id
        self.product_id         = product_id
        self.session_id         = session_id

    def __repr__(self) -> str:
        return f'{self.transaction_id} ({self.order_id}) ({self.product_id}) ({self.session_id})'

class PostgresClient:
    
    engine      = None
    session     = None

    def __init__(self, user_name, password, host, port, db) -> None:
        url = f'postgresql://{user_name}:{password}@{host}:{port}/{db}'
        if not database_exists(url):
            logging.info('Creating database')
            create_database(url)
        logging.info('attaching engine to url')
        self.engine = create_engine(url)
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add(self, entry):
        self.session.add(entry)
        self.session.commit()

    def query(self, object):
        results = self.session.query(object).all()
        return results
    
    def session_commit(self):
        self.session.commit()
    
if __name__ == '__main__':
    ## SEED DATABASE
    ##------------------------------
    psql_client = PostgresClient('lukemason', 'Lukrative11!', 'localhost', '5432', 'bullpen')

    stadiums        = []
    teams           = []
    vendors         = []
    menu_options    = []
    products        = []

    ## Products
    ##------------------------------

    bud_light       = Product('Bud Light - 16oz', 8.00)
    coors_light     = Product('Coors Light - 16oz', 6.50)
    miller_light    = Product('Miller Light - 16oz', 7.50)
    montucky        = Product('Montucky - 16oz', 8.50)
    voodoo_ranger   = Product('Voodoo Ranger - 16oz', 10.00)

    products = [bud_light, coors_light, miller_light, montucky, voodoo_ranger]

    ## Arizona Teams
    ##------------------------------

    # stadium
    footprint_center    = Stadium('Footprint Center')
    chase_field         = Stadium('Chase Field')
    state_farm_stadium  = Stadium('State Farm Stadium')
    stadiums.extend([footprint_center, chase_field, state_farm_stadium])

    # team
    arizona_cardinals       = Team(state_farm_stadium.stadium_id, 'Arizona Cardinals')
    arizona_diamondbacks    = Team(chase_field.stadium_id, 'Arizona Diamondbacks')
    phoenix_suns            = Team(footprint_center.stadium_id, 'Phoenix Suns')
    teams.extend([arizona_cardinals, arizona_diamondbacks, phoenix_suns])

    # vendor
    vendor_one      = Vendor('vendor_one', footprint_center.stadium_id)
    vendor_two      = Vendor('vendor_two', chase_field.stadium_id)
    vendor_three    = Vendor('vendor_three', state_farm_stadium.stadium_id)
    vendors.extend([vendor_one, vendor_two, vendor_three])

    # menu
    vendor_one_bud_light        = MenuOption(vendor_one.vendor_id, bud_light.product_id)
    vendor_one_coors_light      = MenuOption(vendor_one.vendor_id, coors_light.product_id)
    vendor_one_miller_light     = MenuOption(vendor_one.vendor_id, miller_light.product_id)
    vendor_one_voodoo_ranger    = MenuOption(vendor_one.vendor_id, voodoo_ranger.product_id)

    vendor_two_bud_light        = MenuOption(vendor_two.vendor_id, bud_light.product_id)
    vendor_two_montucky         = MenuOption(vendor_two.vendor_id, montucky.product_id)
    vendor_two_voodoo_ranger    = MenuOption(vendor_two.vendor_id, voodoo_ranger.product_id)

    vendor_three_bud_light        = MenuOption(vendor_three.vendor_id, bud_light.product_id)
    vendor_three_voodoo_ranger    = MenuOption(vendor_three.vendor_id, voodoo_ranger.product_id)

    menu_options.extend([vendor_one_bud_light, vendor_one_coors_light, vendor_one_miller_light, vendor_one_voodoo_ranger,
                         vendor_two_bud_light, vendor_two_montucky, vendor_two_voodoo_ranger,
                         vendor_three_bud_light, vendor_three_voodoo_ranger])

    ## Washington Teams
    ##------------------------------

    # stadium
    lumen_field             = Stadium('Lumen Field')
    t_mobile_park           = Stadium('T-Mobile Park')
    climate_pledge_arena    = Stadium('Climate Pledge Arena')
    stadiums.extend([lumen_field, t_mobile_park, climate_pledge_arena])

    # team
    seattle_seahawks        = Team(lumen_field.stadium_id, 'Seattle Seahawks')
    seattle_mariners        = Team(t_mobile_park.stadium_id, 'Seattle Mariners')
    seattle_kraken          = Team(climate_pledge_arena.stadium_id, 'Seattle Kraken')
    teams.extend([seattle_seahawks, seattle_mariners, seattle_kraken])

    # vendor
    vendor_four         = Vendor('vendor_four', seattle_seahawks.stadium_id)
    vendor_five         = Vendor('vendor_five', seattle_mariners.stadium_id)
    vendor_six          = Vendor('vendor_six', seattle_kraken.stadium_id)
    vendors.extend([vendor_four, vendor_five, vendor_six])

    # menu
    vendor_four_coors_light      = MenuOption(vendor_four.vendor_id, coors_light.product_id)
    vendor_four_miller_light     = MenuOption(vendor_four.vendor_id, miller_light.product_id)

    vendor_five_bud_light        = MenuOption(vendor_five.vendor_id, bud_light.product_id)
    vendor_five_montucky         = MenuOption(vendor_five.vendor_id, montucky.product_id)

    vendor_six_miller_light     = MenuOption(vendor_six.vendor_id, miller_light.product_id)
    vendor_six_voodoo_ranger    = MenuOption(vendor_six.vendor_id, voodoo_ranger.product_id)

    menu_options.extend([vendor_four_coors_light, vendor_four_miller_light,
                         vendor_five_bud_light, vendor_five_montucky,
                         vendor_six_miller_light, vendor_six_voodoo_ranger])

    ## Colorado Teams
    ##------------------------------

    # stadium
    empower_field_at_mile_high      = Stadium('Empower Field at Mile High')
    coors_field                     = Stadium('Coors Field')
    ball_arena                      = Stadium('Ball Arena')
    stadiums.extend([empower_field_at_mile_high, coors_field, ball_arena])

    # team
    denver_broncos          = Team(empower_field_at_mile_high.stadium_id, 'Denver Broncos')
    colorado_rockies        = Team(coors_field.stadium_id, 'Colorado Rockies')
    denver_nuggets          = Team(ball_arena.stadium_id, 'Denver Nuggets')
    teams.extend([denver_broncos, colorado_rockies, denver_nuggets])

    # vendor
    vendor_seven        = Vendor('vendor_seven', empower_field_at_mile_high.stadium_id)
    vendor_eight        = Vendor('vendor_eight', coors_field.stadium_id)
    vendor_nine         = Vendor('vendor_nine', ball_arena.stadium_id)
    vendors.extend([vendor_seven, vendor_eight, vendor_nine])

    # menu
    vendor_seven_coors_light        = MenuOption(vendor_seven.vendor_id, coors_light.product_id)
    vendor_seven_miller_light       = MenuOption(vendor_seven.vendor_id, miller_light.product_id)

    vendor_eight_coors_light        = MenuOption(vendor_eight.vendor_id, coors_light.product_id)
    vendor_eight_miller_light       = MenuOption(vendor_eight.vendor_id, miller_light.product_id)
    vendor_eight_montucky           = MenuOption(vendor_eight.vendor_id, montucky.product_id)

    vendor_nine_voodoo_ranger       = MenuOption(vendor_nine.vendor_id, voodoo_ranger.product_id)

    menu_options.extend([vendor_seven_coors_light, vendor_seven_miller_light,
                         vendor_eight_coors_light, vendor_eight_miller_light, vendor_eight_montucky,
                         vendor_nine_voodoo_ranger])

    ## Georgia Teams
    ##------------------------------

    # stadium
    mercedes_benz_stadium       = Stadium('Mercedes-Benz Stadium')
    truist_park                 = Stadium('Truist Park')
    state_farm_arena            = Stadium('State Farm Arena')
    stadiums.extend([mercedes_benz_stadium, truist_park, state_farm_arena])

    # team
    atlanta_falcons         = Team(mercedes_benz_stadium.stadium_id, 'Atlanta Falcons')
    atlanta_braves          = Team(truist_park.stadium_id, 'Atlanta Braves')
    atlanta_hawks           = Team(state_farm_arena.stadium_id, 'Atlanta Hawks')
    teams.extend([atlanta_falcons, atlanta_braves, atlanta_hawks])

    # vendor
    vendor_ten          = Vendor('vendor_ten', mercedes_benz_stadium.stadium_id)
    vendor_eleven       = Vendor('vendor_eleven', truist_park.stadium_id)
    vendor_twelve       = Vendor('vendor_twelve', state_farm_arena.stadium_id)
    vendors.extend([vendor_ten, vendor_eleven, vendor_twelve])

    # menu
    vendor_ten_bud_light        = MenuOption(vendor_ten.vendor_id, bud_light.product_id)
    vendor_ten_coors_light      = MenuOption(vendor_ten.vendor_id, coors_light.product_id)
    vendor_ten_miller_light     = MenuOption(vendor_ten.vendor_id, miller_light.product_id)
    vendor_ten_voodoo_ranger    = MenuOption(vendor_ten.vendor_id, voodoo_ranger.product_id)

    vendor_eleven_bud_light        = MenuOption(vendor_eleven.vendor_id, bud_light.product_id)
    vendor_eleven_montucky         = MenuOption(vendor_eleven.vendor_id, montucky.product_id)
    vendor_eleven_voodoo_ranger    = MenuOption(vendor_eleven.vendor_id, voodoo_ranger.product_id)

    vendor_twelve_bud_light        = MenuOption(vendor_twelve.vendor_id, bud_light.product_id)
    vendor_twelve_voodoo_ranger    = MenuOption(vendor_twelve.vendor_id, voodoo_ranger.product_id)

    menu_options.extend([vendor_ten_bud_light, vendor_ten_coors_light, vendor_ten_miller_light, vendor_ten_voodoo_ranger,
                         vendor_eleven_bud_light, vendor_eleven_montucky, vendor_eleven_voodoo_ranger,
                         vendor_twelve_bud_light, vendor_twelve_voodoo_ranger])
    
    session_zero = Session(datetime.now(), 'session_zero', arizona_cardinals.team_id ,True)

    # ## SEED VALUES
    # ##------------------------------
    # for product in products:
    #     psql_client.add(product)

    # for stadium in stadiums:
    #     psql_client.add(stadium)

    # for team in teams:
    #     psql_client.add(team)

    # for vendor in vendors:
    #     psql_client.add(vendor)

    # for option in menu_options:
    #     psql_client.add(option)
