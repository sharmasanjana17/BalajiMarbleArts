"""
Database initialization and management utilities
"""
from src.models import db, Project, Service, Material, Finish, Testimonial, BlogPost, FAQ, ContactLead
from datetime import datetime, date
from sqlalchemy import text

def migrate_database(app):
    """Add missing columns to tables if they don't exist"""
    with app.app_context():
        try:
            # Check and add videos column to projects table
            result = db.session.execute(text("PRAGMA table_info(projects)"))
            columns = [row[1] for row in result]
            
            if 'videos' not in columns:
                print("Adding 'videos' column to projects table...")
                db.session.execute(text("ALTER TABLE projects ADD COLUMN videos TEXT"))
                db.session.commit()
                print("✅ Videos column added successfully!")
            else:
                print("✅ Videos column already exists!")
            
            # Check and add images column to testimonials table
            result = db.session.execute(text("PRAGMA table_info(testimonials)"))
            columns = [row[1] for row in result]
            
            if 'images' not in columns:
                print("Adding 'images' column to testimonials table...")
                db.session.execute(text("ALTER TABLE testimonials ADD COLUMN images TEXT"))
                db.session.commit()
                print("✅ Images column added to testimonials table successfully!")
            else:
                print("✅ Images column already exists in testimonials table!")
            
            # Check and add images column to blog_posts table
            result = db.session.execute(text("PRAGMA table_info(blog_posts)"))
            columns = [row[1] for row in result]
            
            if 'images' not in columns:
                print("Adding 'images' column to blog_posts table...")
                db.session.execute(text("ALTER TABLE blog_posts ADD COLUMN images TEXT"))
                db.session.commit()
                print("✅ Images column added to blog_posts table successfully!")
            else:
                print("✅ Images column already exists in blog_posts table!")
                
        except Exception as e:
            print(f"Database migration check: {e}")
            db.session.rollback()

def init_database(app):
    """Initialize database with sample data"""
    with app.app_context():
        # First, migrate existing database (add videos column if needed)
        migrate_database(app)
        
        # Drop all tables (for fresh start)
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Sample Services
        services = [
            Service(name='Marble Flooring', description='Professional marble flooring installation for residential and commercial spaces', icon='floor', benefits='Durable, Elegant, Easy maintenance'),
            Service(name='Wall Cladding', description='Premium marble wall cladding solutions', icon='wall', benefits='Modern look, Weather resistant, Long lasting'),
            Service(name='Feature Walls', description='Stunning marble feature walls for interior spaces', icon='feature', benefits='Aesthetic appeal, Unique design, High value'),
            Service(name='Staircases', description='Elegant marble staircase installation', icon='stairs', benefits='Luxury finish, Slip resistant, Durable'),
            Service(name='Countertops', description='Premium marble countertops for kitchens and bathrooms', icon='counter', benefits='Heat resistant, Easy to clean, Beautiful'),
            Service(name='Exterior Cladding', description='Weather-resistant marble exterior cladding', icon='exterior', benefits='Weather proof, Low maintenance, Premium look'),
            Service(name='Bathroom Marble Work', description='Complete bathroom marble solutions', icon='bathroom', benefits='Water resistant, Hygienic, Elegant'),
            Service(name='Custom Design Work', description='Bespoke marble design and installation', icon='custom', benefits='Unique designs, Tailored solutions, Expert craftsmanship')
        ]
        
        for service in services:
            db.session.add(service)
        
        # Sample Materials
        materials = [
            Material(
                name='Statuario Italian Marble',
                type='Marble',
                origin='Carrara, Italy',
                characteristics='{"color": "Bright pure white with dramatic grey & gold veins", "pattern": "Bold diagonal veining, feather edges", "texture": "Fine-grained, mirror-reflective"}',
                images='marble-statuario.jpg',
                finishes='polished,honed',
                best_use_cases='Master Living Room, Feature Walls, Luxury Foyers, Designer Bathrooms',
                durability='High',
                price_range='Ultra Luxury (₹600 - ₹2,500/sq.ft)',
                maintenance='Annual sealing and pH-neutral marble cleaner recommended',
                description='The pinnacle of Italian luxury marble. Statuario is celebrated worldwide for its crisp white background and bold, dramatic grey and gold ribbons.'
            ),
            Material(
                name='Makrana Pure White Marble',
                type='Marble',
                origin='Makrana, Rajasthan, India',
                characteristics='{"color": "Pure milky white with soft crystalline luster", "pattern": "Natural subtle clouds, Taj Mahal grade", "texture": "99% pure calcium carbonate, non-porous"}',
                images='marble-makrana.jpg',
                finishes='polished,honed',
                best_use_cases='Pooja Mandir, Palatial Courtyards, Living Rooms, Heritage Monuments',
                durability='Lifetime (Never yellows or loses polish)',
                price_range='Premium (₹250 - ₹1,200/sq.ft)',
                maintenance='Extremely low maintenance, washes clean with water, gains luster with age',
                description='The world-famous marble used to construct the Taj Mahal and Victoria Memorial. Mined from the historic quarries of Makrana, it never loses its polish.'
            ),
            Material(
                name='Nero Marquina Black Marble',
                type='Marble',
                origin='Markina, Spain / India',
                characteristics='{"color": "Deep velvety black with crisp white calcite veins", "pattern": "High-contrast geometric and lightning veining", "texture": "Dense, fine-grained"}',
                images='marble-nero-marquina.jpg',
                finishes='polished,honed,brushed',
                best_use_cases='Vanity Tops, Fireplace Facades, Bar Counters, Contrast Border Inlays',
                durability='High',
                price_range='Premium (₹350 - ₹900/sq.ft)',
                maintenance='Regular sealing against acid stains',
                description='A striking black marble with intense white fracture lines. Nero Marquina brings bold theatrical contrast and modern architectural elegance to feature spaces.'
            ),
            Material(
                name='Calacatta Gold Italian Marble',
                type='Marble',
                origin='Carrara, Tuscany, Italy',
                characteristics='{"color": "Warm ivory white with honey-gold and smoky taupe ribbons", "pattern": "Thick, expressive ribbon veining", "texture": "Lustrous crystalline marble"}',
                images='marble-calacatta.jpg',
                finishes='polished,honed',
                best_use_cases='Waterfall Kitchen Islands, Master En-suites, Bookmatched Wall Cladding',
                durability='High',
                price_range='Ultra Luxury (₹750 - ₹3,000/sq.ft)',
                maintenance='Premium penetrating sealer application twice a year',
                description='Rarer than standard Carrara, Calacatta Gold features creamy warm tones intertwined with opulent golden-amber veins, creating a majestic statement.'
            ),
            Material(
                name='Italian Carrara Marble',
                type='Marble',
                origin='Carrara, Italy',
                characteristics='{"color": "Cool off-white with feather-soft graphite veining", "pattern": "Subtle, smoky, timeless Roman veining", "texture": "Fine-grained classic marble"}',
                images='marble-carrara.jpg',
                finishes='polished,honed',
                best_use_cases='Living Room Flooring, Wall Cladding, Bathrooms, Classic Sculptures',
                durability='High',
                price_range='Premium (₹350 - ₹850/sq.ft)',
                maintenance='Regular cleaning with stone-safe soap and periodic sealing',
                description='The classic benchmark of Roman stonecraft favored by Michelangelo, famous for its delicate smoky feathers over a luminous white base.'
            ),
            Material(
                name='Bottochino Classic Beige Marble',
                type='Marble',
                origin='Brescia, Lombardy, Italy',
                characteristics='{"color": "Warm creamy beige with hazelnut clouds and pearl veins", "pattern": "Gentle tonal clouds, warm golden-hazelnut wisps", "texture": "Compact, dense limestone marble"}',
                images='marble-bottochino.jpg',
                finishes='polished,honed',
                best_use_cases='Grand Hallways, Hotel Lobbies, Seamless Living Areas, Staircases',
                durability='High',
                price_range='Premium (₹280 - ₹650/sq.ft)',
                maintenance='Standard marble sealing, very forgiving with dust and footprints',
                description='An enduring Italian favorite offering warm, honey-beige hues that reflect sunlight gracefully and create a royal European ambience.'
            ),
            Material(
                name='Udaipur Green Marble (Verde Guatemala)',
                type='Marble',
                origin='Udaipur, Rajasthan, India',
                characteristics='{"color": "Deep forest emerald green with dense serpentine web", "pattern": "Intricate network of dark green, black and white veins", "texture": "Dense, metamorphic serpentine stone"}',
                images='marble-green.jpg',
                finishes='polished,honed,leathered',
                best_use_cases='Bathroom Cladding, Temple Steps, Countertops, Outdoor Water Features, Table Tops',
                durability='Very High',
                price_range='Affordable to Moderate (₹120 - ₹350/sq.ft)',
                maintenance='Naturally moisture-resistant, minimal upkeep required',
                description='Mined from the mineral-rich Aravalli range of Udaipur, this dense serpentine green marble is revered globally for its regal emerald depths and water resistance.'
            ),
            Material(
                name='Rainforest Golden Marble (Bidasar)',
                type='Marble',
                origin='Bidasar, Rajasthan, India',
                characteristics='{"color": "Warm golden-brown base with dark chocolate & crimson branches", "pattern": "Tree roots, organic branch networks, nature artwork", "texture": "Serpentine with crystalline quartz veins"}',
                images='marble-rainforest.jpg',
                finishes='polished,honed,brushed,leathered',
                best_use_cases='Feature Walls, Bar Facings, Conference Tabletops, Elevator Lobbies',
                durability='High',
                price_range='Premium (₹180 - ₹450/sq.ft)',
                maintenance='Periodic sealing recommended for polished surfaces',
                description='Nature’s own canvas. Mined exclusively in Rajasthan, Bidasar Golden marble features an arresting root-and-branch pattern mimicking rainforest canopies.'
            ),
            Material(
                name='Honey Onyx Translucent Marble',
                type='Marble',
                origin='Baluchistan / Turkey',
                characteristics='{"color": "Translucent amber, honey, butterscotch and warm cream", "pattern": "Parallel concentric banded crystalline layers", "texture": "Semiprecious cryptocrystalline chalcedony / calcite"}',
                images='marble-onyx.jpg',
                finishes='polished',
                best_use_cases='Backlit Bar Counters, Reception Desks, Luxury Powder Rooms, Wall Paneling',
                durability='Medium (Internal decorative marvel)',
                price_range='Ultra Luxury (₹800 - ₹3,500/sq.ft)',
                maintenance='Avoid acids, clean with microfiber and distilled water',
                description='A breathtaking semi-precious stone that transmits light. When backlit by LED panels, Honey Onyx glows with warm golden radiance as an artistic centerpiece.'
            ),
            Material(
                name='Roman Travertine Beige Marble',
                type='Marble',
                origin='Tivoli, Italy / Turkey',
                characteristics='{"color": "Warm cream, walnut and caramel horizontal strata", "pattern": "Linear sedimentary bedding with natural micro-pores", "texture": "Porous terrestrial limestone, filled or unfilled"}',
                images='marble-travertine.jpg',
                finishes='honed,brushed,polished',
                best_use_cases='Exterior Cladding, Pool Decks, Tuscan Bathrooms, Living Accent Walls',
                durability='High',
                price_range='Premium (₹250 - ₹600/sq.ft)',
                maintenance='Penetrating sealer required; naturally slip-resistant',
                description='The historic stone of the Roman Colosseum and St. Peter’s Square, delivering rustic Old-World grandeur, linear strata textures, and superb thermal comfort.'
            ),
            Material(
                name='Black Galaxy Granite',
                type='Granite',
                origin='Ongole, Andhra Pradesh, India',
                characteristics='{"color": "Pitch black base with thousands of sparkling golden flecks", "pattern": "Starry cosmos effect from bronzite crystal inclusions", "texture": "Ultra-hard, non-porous igneous rock"}',
                images='granite-black-galaxy.jpg',
                finishes='polished,leathered,honed',
                best_use_cases='Kitchen Countertops, High-Traffic Stairs, Commercial Entrances, Vanity Slabs',
                durability='Extreme (Scratch, Stain & Heat Proof)',
                price_range='Moderate (₹180 - ₹400/sq.ft)',
                maintenance='Virtually zero maintenance, wipe clean with soapy water',
                description='India’s most celebrated export granite. With reflective golden crystals embedded in deep jet black, it resembles a glittering night sky while offering extreme durability.'
            ),
            Material(
                name='Kashmir White Granite',
                type='Granite',
                origin='Madurai, Tamil Nadu, India',
                characteristics='{"color": "Luminous silver-white ground with soft grey waves & garnet crystals", "pattern": "Subtle river movement with deep burgundy garnet jewels", "texture": "Medium-grained hard crystalline granite"}',
                images='granite-kashmir-white.jpg',
                finishes='polished,honed,leathered',
                best_use_cases='Modern Kitchen Countertops, Bright Living Slabs, Vanity Counters',
                durability='Very High',
                price_range='Moderate (₹160 - ₹380/sq.ft)',
                maintenance='Apply penetrating stone sealer once a year',
                description='Bright and airy, Kashmir White illuminates contemporary interiors. Its frosty white field is adorned with delicate slate currents and rich wine-colored garnet crystals.'
            ),
            Material(
                name='Kota Stone Blue-Green',
                type='Marble',
                origin='Kota, Rajasthan, India',
                characteristics='{"color": "Natural bluish green with subtle earthy mineral bands", "pattern": "Uniform fine-grained sedimentary stone", "texture": "Tough, non-slip, natural cooling surface"}',
                images='marble-kota.jpg',
                finishes='polished,honed,brushed',
                best_use_cases='Verandahs, Corridors, Garden Walkways, Porches, Commercial Basements',
                durability='Very High',
                price_range='Budget-Friendly (₹45 - ₹120/sq.ft)',
                maintenance='Extremely rugged, withstands harsh weather and heavy foot traffic',
                description='The workhorse of Indian stone architecture. Kota stone is cool under bare feet, naturally slip-resistant, and virtually indestructible.'
            ),
            Material(
                name='Rosa Norvegia / Ambaji Pink Marble',
                type='Marble',
                origin='Ambaji, Gujarat / Makrana, India',
                characteristics='{"color": "Soft blush pastel pink with delicate cream & rose veining", "pattern": "Gentle flowing cloud waves and rosy ribbons", "texture": "Fine crystalline metamorphic marble"}',
                images='marble-pink.jpg',
                finishes='polished,honed',
                best_use_cases='Master Bedrooms, Spa Bathrooms, Traditional Pillars, Jali Partitions',
                durability='High',
                price_range='Moderate (₹110 - ₹280/sq.ft)',
                maintenance='Standard marble care with periodic buffing',
                description='Evoking subtle royal warmth, Indian Pink marble combines soothing pastel tones with delicate rose veins, creating a serene, peaceful sanctuary.'
            )
        ]
        
        for material in materials:
            db.session.add(material)
        
        # Real Contractor Projects with Actual Photos
        projects = [
            Project(
                title='Luxury Villa Italian Marble Flooring & Diamond Mirror Polishing',
                description='High-gloss mirror-finish Italian marble flooring installed with seamless epoxy grouting and multi-stage diamond polishing. Features custom border inlay work and massive round marble foyer columns. The surface exhibits a 95+ gloss unit mirror reflection without lippage.',
                short_description='Seamless mirror-finish Italian marble flooring with diamond polishing',
                category='Residential,Flooring',
                location='South Delhi & DLF Phase 5, Gurgaon',
                client_type='Residential',
                images='flooring-mirror-polish-1.jpg,flooring-mirror-polish-2.jpg,flooring-mirror-polish-3.jpg,flooring-mirror-polish-4.jpg,flooring-hallway-columns.jpg,flooring-bookmatched-living.jpg',
                videos='',
                materials='Italian Statuario, Grey William, Bottochino, Epoxy Joint Filler',
                status='completed',
                featured=True,
                completion_date=date(2024, 10, 15)
            ),
            Project(
                title='Handcrafted Makrana Marble Pooja Mandir & Sacred Spaces',
                description='Complete sacred prayer sanctuary featuring pure white Makrana marble carved pillars, multi-tier shikhar dome, hand-carved floral jaali panels, modern backlit lotus feature wall, and inlaid marble floor carpet. Meticulously handcrafted by master artisans.',
                short_description='Pure white Makrana marble temple with carved pillars and backlit lotus altar',
                category='Residential,Temple Work',
                location='Jaipur & Delhi NCR',
                client_type='Residential',
                images='mandir-makrana-sanctuary-1.jpg,mandir-makrana-sanctuary-2.jpg,mandir-modern-lotus-backlit.jpg,mandir-om-lotus-backlit.jpg,mandir-carved-dome-stepped.jpg,mandir-dome-ceiling-lighting.jpg,mandir-grand-temple-room.jpg',
                videos='',
                materials='Pure Makrana White Marble, Brass Hardware, LED Warm Backlighting',
                status='completed',
                featured=True,
                completion_date=date(2024, 9, 20)
            ),
            Project(
                title='Architectural Curved & Cantilevered Marble Staircases',
                description='Seamless curved and floating marble stairs featuring Bottochino and Grey Italian marble with precision groove anti-skid detailing, concealed under-step LED lighting strips, and structural glass balustrade mounts. Engineered for structural rigidity and aesthetic elegance.',
                short_description='Helical cantilevered marble stairs with embedded LED profile lighting',
                category='Residential,Staircases',
                location='Greater Kailash, Delhi',
                client_type='Residential',
                images='stairs-curved-led-lighting-1.jpg,stairs-curved-led-lighting-2.jpg,stairs-bottochino-grooved-1.jpg,stairs-bottochino-grooved-2.jpg,stairs-white-black-riser.jpg,stairs-gold-lotus-inlay.jpg,stairs-spiral-ornamental.jpg',
                materials='Bottochino Marble, Black Marquina Risers, Profile LED Strips',
                status='completed',
                featured=True,
                completion_date=date(2024, 8, 10)
            ),
            Project(
                title='Master Ensuite Statuario Marble Bathrooms & Illuminated Onyx Vanities',
                description='Ultra-luxury ensuite bathrooms fitted with bookmatched Italian Statuario marble wall cladding, integrated jacuzzi encasement, walk-in shower niches, and custom-lit translucent Honey Onyx stone vanities. Complete with precision mitered joints and waterproof stone sealing.',
                short_description='Bookmatched Statuario cladding, jacuzzi encasement & backlit Onyx vanities',
                category='Residential,Bathrooms',
                location='DLF Phase 5, Gurgaon',
                client_type='Residential',
                images='bathroom-statuario-ensuite-1.jpg,bathroom-statuario-ensuite-2.jpg,bathroom-statuario-shower.jpg,bathroom-onyx-illuminated-vanity.jpg,bathroom-onyx-backlit-counter.jpg,bathroom-travertine-vanity-basin.jpg,bathroom-green-onyx-shower.jpg',
                materials='Italian Statuario Marble, Translucent Honey Onyx, Roman Travertine',
                status='completed',
                featured=True,
                completion_date=date(2024, 7, 5)
            ),
            Project(
                title='Classical Villa Exterior Stone Elevation & Architectural Facades',
                description='Complete building facade treatment with grooved stone wall cladding, classical window architraves, fluted pilasters, carved entrance gate pillars, and weather-resistant stone elevation detailing. Built to withstand environmental exposure while maintaining timeless classical grandeur.',
                short_description='Grooved stone wall cladding, window architraves, pilasters & gate pillars',
                category='Commercial,Exterior Cladding',
                location='Chandigarh & Delhi NCR',
                client_type='Commercial',
                images='elevation-villa-facade-full.jpg,elevation-arched-window-molding.jpg,elevation-window-pilaster.jpg,elevation-gate-pillars-arch.jpg,elevation-balcony-cladding.jpg,elevation-carved-column-base.jpg',
                materials='Beige Sandstone, Roman Travertine, Carved Granite Bases',
                status='completed',
                featured=True,
                completion_date=date(2024, 6, 15)
            ),
            Project(
                title='Handcrafted Marble Inlay & Pietra Dura Artistry',
                description='Exquisite traditional craftsmanship featuring semi-precious stone lotus motifs, Tree of Life wall murals, Mother of Pearl floral door panels, custom Ganesha medallions, and continuous acanthus carpet runners. Each piece is hand-carved and inlaid by hereditary artisans.',
                short_description='Semi-precious stone Pietra Dura inlay, Tree of Life mural & MOP medallions',
                category='Residential,Inlay & Carving',
                location='Agra & Jaipur Craftsmanship',
                client_type='Residential',
                images='inlay-lotus-pietra-dura.jpg,inlay-tree-of-life-mural.jpg,inlay-carpet-runner-hallway.jpg,inlay-ganesha-mop-medallion.jpg,inlay-floral-pietra-medallion.jpg,inlay-artisan-craftsman-work.jpg,inlay-mop-door-panels.jpg',
                materials='Makrana White Marble, Semi-Precious Stones, Mother of Pearl, Malachite',
                status='completed',
                featured=True,
                completion_date=date(2024, 5, 20)
            )
        ]
        
        for project in projects:
            db.session.add(project)
        
        # Sample Finishes
        finishes = [
            Finish(
                name='Polished Finish',
                description='High-gloss, reflective surface that enhances the natural beauty of marble',
                images='polished.jpg',
                characteristics='Glossy,Reflective,Smooth',
                benefits='Easy to clean,Enhances color,Luxurious appearance',
                applications='Flooring,Wall cladding,Countertops',
                maintenance='Requires regular polishing to maintain shine'
            ),
            Finish(
                name='Honed Finish',
                description='Matte, smooth surface with no shine, providing a contemporary look',
                images='honed.jpg',
                characteristics='Matte,Smooth,Non-reflective',
                benefits='Slip-resistant,Hides scratches,Modern aesthetic',
                applications='Flooring,Bathroom walls,Outdoor areas',
                maintenance='Low maintenance, easy to clean'
            ),
            Finish(
                name='Brushed Finish',
                description='Textured surface with subtle brush marks, providing a rustic elegant look',
                images='brushed.jpg',
                characteristics='Textured,Matte,Natural',
                benefits='Slip-resistant,Unique texture,Low maintenance',
                applications='Flooring,Outdoor areas,Feature walls',
                maintenance='Easy to clean, no special care required'
            )
        ]
        
        for finish in finishes:
            db.session.add(finish)
        
        # Sample FAQs
        faqs = [
            FAQ(
                category='Marble Selection',
                question='How to choose the right marble?',
                answer='When choosing marble, consider factors like usage area, foot traffic, maintenance requirements, and budget. For high-traffic areas, opt for harder marble varieties like Kota or Italian marble. For decorative purposes, you can choose more delicate varieties.',
                order=1
            ),
            FAQ(
                category='Installation Process',
                question='How long does installation take?',
                answer='Installation time varies based on project size. A typical residential flooring project takes 3-7 days, while larger commercial projects may take 2-4 weeks. We provide detailed timelines during the consultation.',
                order=1
            ),
            FAQ(
                category='Maintenance & Care',
                question='How to maintain marble?',
                answer='Regular cleaning with pH-neutral cleaners, immediate spill cleanup, and periodic sealing (every 6-12 months) will keep your marble looking beautiful. Avoid acidic cleaners and use coasters under glasses.',
                order=1
            ),
            FAQ(
                category='Cost & Pricing',
                question='How much does marble installation cost?',
                answer='Cost depends on material type, area size, finish, and complexity. Basic marble flooring starts around ₹100-200 per sq ft, while premium Italian marble can cost ₹500-1000+ per sq ft. We provide detailed quotes after site visit.',
                order=1
            )
        ]
        
        for faq in faqs:
            db.session.add(faq)
        
        # Sample Testimonials
        testimonials = [
            Testimonial(
                client_name='Rajesh Kumar',
                location='Indiranagar, Bengaluru',
                rating=5,
                text='Balaji Marble Arts transformed our villa with exquisite Italian marble flooring. Ashok ji and his team are true craftsmen. Highly recommended!',
                project_id=1
            ),
            Testimonial(
                client_name='Priya Sundaram (Architect)',
                location='Whitefield, Bengaluru',
                rating=5,
                text='We have collaborated with Balaji Marble Arts on multiple commercial and residential projects. Their attention to detail and timely handover is unmatched.',
                project_id=2
            ),
            Testimonial(
                client_name='Vikram Malhotra',
                location='Koramangala, Bengaluru',
                rating=5,
                text='Top quality Italian Carrara marble countertop installation in our kitchen. Seamless joints, perfect edge profile, and great polish!',
                project_id=3
            ),
            Testimonial(
                client_name='Ananya Reddy',
                location='Jayanagar, Bengaluru',
                rating=5,
                text='The grand marble staircase crafted by Ashok Sharma ji became the centerpiece of our home. Outstanding craftsmanship and very polite team.',
                project_id=4
            )
        ]
        
        for testimonial in testimonials:
            db.session.add(testimonial)
        
        # Commit all changes
        db.session.commit()
        
        # Sample Blog Posts with Images
        blog_posts = [
            BlogPost(
                title='Choosing the Right Marble for Your Home',
                slug='choosing-right-marble-home',
                category='Marble Selection',
                author='Ashok Sharma',
                published_date=date(2024, 11, 1),
                featured_image='blog-1.jpg',
                excerpt='A comprehensive guide to selecting the perfect marble for your home renovation project.',
                content='<p>Marble selection is crucial for any home renovation project...</p>',
                tags='marble,selection,home,renovation',
                seo_keywords='marble selection, home renovation, marble types'
            ),
            BlogPost(
                title='Marble Maintenance Tips',
                slug='marble-maintenance-tips',
                category='Maintenance',
                author='Ashok Sharma',
                published_date=date(2024, 10, 15),
                featured_image='blog-2.jpg',
                excerpt='Essential tips to keep your marble looking beautiful for years to come.',
                content='<p>Proper maintenance is key to preserving marble beauty...</p>',
                tags='marble,maintenance,care,tips',
                seo_keywords='marble maintenance, marble care, cleaning marble'
            ),
            BlogPost(
                title='Latest Marble Design Trends 2024',
                slug='marble-design-trends-2024',
                category='Design Trends',
                author='Ashok Sharma',
                published_date=date(2024, 9, 20),
                featured_image='blog-3.jpg',
                excerpt='Discover the latest marble design trends shaping modern interiors.',
                content='<p>Marble design trends are evolving...</p>',
                tags='marble,design,trends,2024',
                seo_keywords='marble trends, design trends, modern marble'
            )
        ]
        
        for post in blog_posts:
            db.session.add(post)
        
        # Commit all changes
        db.session.commit()
        
        print("Database initialized successfully!")
        print(f"Created {len(services)} services, {len(materials)} materials, {len(finishes)} finishes, {len(projects)} projects, {len(blog_posts)} blog posts, {len(faqs)} FAQs")

