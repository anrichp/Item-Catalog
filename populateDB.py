from app import db
from app.models import Item, Category

category1 = Category(name="Canon")
category2 = Category(name="Nikon")
category3 = Category(name="Pentax")
category4 = Category(name="Sony")
category5 = Category(name="Olympus")
category6 = Category(name="Fujifilm")
category7 = Category(name="GoPro")
category8 = Category(name="Leica")

db.session.add(category1)
db.session.add(category2)
db.session.add(category3)
db.session.add(category4)
db.session.add(category5)
db.session.add(category6)
db.session.add(category7)
db.session.add(category8)

item1 = Item(name="Canon Rebel SL2",
             description='''Best all-round: Canon's smallest DSLR blends
                            versatility and value.''',
             category=category1)
item2 = Item(name="Canon EOS R",
             description='''Runner-up: Canon's first full-frame mirrorless
                            camera means business''',
             category=category1)
item3 = Item(name="Canon EOS 5D Mark IV",
             description='''From the moment light passes through the lens,the
                            EOS 5D Mark IV captures every nuance, every colour,
                            every detail.''',
             category=category1)

item4 = Item(name="Nikon D3X",
             description='''The Nikon D3X is a 24.4-megapixel professional
                            -grade full-frame digital single-lens
                            reflex camera''',
             category=category2)

item5 = Item(name="Nikon D2Xs",
             description='''find out how the D2Xs stacks up against the
                            competition in our real-world review with
                            in-depth image quality comparisons.''',
             category=category2)

item6 = Item(name="Sony A580",
             description='''The 16.2MP Sony A580 is based around one of the
                          company's Exmor APS HD CMOS sensors''',
             category=category4)

item7 = Item(name="Pentax 645Z",
             description='''The Pentax 645Z is a professional medium format
                            digital SLR camera announced by Ricoh''',
             category=category3)
item8 = Item(name="Pentax K-1",
             description='''Sporting Pentax's first full-frame digital image
                            sensor, the K-1 DSLR Camera is a landmark release
                            for the respected company''',
             category=category3)

item9 = Item(name="Olympus OM-D E‑M5",
             description='''The Olympus OM-D E-M1 Mark II is a high performance
                            mirrorless digital camera sporting a 20.4MP
                            live MOS Micro Four Thirds sensor''',
             category=category5)
item10 = Item(name="Olympus OM-D E‑M1",
              description='''Powering the OM-D E-M5 Mark II is Olympus's own 16
                              megapixel Live MOS sensor and TruePic
                              VII image processor''',
              category=category5)

item11 = Item(name="fujifilm xt20",
              description='''The Fujifilm XT 20 mirrorless camera features a
                              2.36M-dot organic EL electronic viewfinder''',
              category=category6)
item12 = Item(name="fujifilm xt2",
              description='''The Fujifilm X-T2 is a compact, lightweight, and
                              high-performance mirrorless camera that includes
                              all the features that a modern
                              photographer needs.''',
              category=category6)
item13 = Item(name="fujifilm x100f",
              description='''The Fujifilm X100F is a powerful premium compact
                              camera with a beautifully designed
                              and compact body.''',
              category=category6)

item14 = Item(name="GoPro HERO5 Black",
              description='''The GoPro HERO5 Black is the ultimate action camera.
                              Everything of the previous camera's been revised,
                              improving video/image quality''',
              category=category7)
item15 = Item(name="GoPro HERO4 Session",
              description='''HERO4 Session packs the power of GoPro into our
                              smallest, lightest, most convenient camera
                              yet—featuring a rugged and waterproof design''',
              category=category7)

item16 = Item(name="Leica SL",
              description='''The Leica SL-System is the embodiment of the
                             digital era in professional photography''',
              category=category8)


db.session.add(item1)
db.session.add(item2)
db.session.add(item3)
db.session.add(item4)
db.session.add(item5)
db.session.add(item6)
db.session.add(item7)
db.session.add(item8)
db.session.add(item9)
db.session.add(item10)
db.session.add(item11)
db.session.add(item12)
db.session.add(item13)
db.session.add(item14)
db.session.add(item15)
db.session.add(item16)

db.session.commit()

print('Added categories')