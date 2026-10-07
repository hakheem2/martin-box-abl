"""Create or refresh Martin Boxabl's four evergreen blog guides."""

from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from wagtail.models import Page
from wagtail.images.models import Image

from blog.models import BlogCategory, BlogIndexPage, BlogPostPage


POSTS = [
    {
        "title": "Modular Homes vs. Traditional Construction: What Buyers Should Compare",
        "slug": "modular-homes-vs-traditional-construction",
        "seo_title": "Modular Homes vs. Traditional Homes: A Buyer’s Guide",
        "search_description": "Compare modular and site-built homes by construction method, schedule, design, site work, and total project cost before you choose.",
        "excerpt": "Modular and site-built homes can both deliver lasting, comfortable living. Compare how they are built, what happens on your land, and which costs and questions matter before you commit.",
        "category": "Home Buying Guides",
        "tags": ["modular homes", "prefab homes", "home buying", "construction"],
        "image": "static/images/homes/home-2.jpg",
        "image_title": "Modern modular home exterior for construction comparison",
        "body": """
<p>Choosing a home is about more than comparing photographs or a headline price. The construction method affects how a project is planned, what work happens at the home site, which professionals need to be involved, and how the final budget comes together. Modular construction and traditional site-built construction can both be good choices; the right fit depends on the home, the land, local requirements, and the buyer’s priorities.</p>
<p>Use this guide to compare the process carefully. Martin Boxabl showcases modern housing options and helps buyers explore the next questions; it does not replace advice from your local building department, lender, surveyor, or licensed contractor.</p>
<h2>What “modular” and “site-built” mean</h2>
<p>A modular home is made in sections in a controlled production setting and transported to a prepared site for placement and completion. “Prefab” is a broader term for components or buildings made before they reach the property. A traditional site-built home is assembled primarily at the property. Product labels vary, so ask the manufacturer exactly what is factory-completed, what arrives on the truck, and what remains to be done locally.</p>
<p>Modular homes should not be confused automatically with manufactured homes. The applicable construction standards and approval process depend on the specific product and jurisdiction. Ask for the code or certification documents that apply to the model you are considering, then verify them with your local authority.</p>
<h2>Compare the full project, not just the home price</h2>
<p>A quoted unit price may not include land, surveys, engineering, permits, foundation work, transport, crane or setting services, utility connections, access improvements, taxes, or finish work. Site-built proposals can also vary in what they include. Put both options on the same written scope before comparing totals.</p>
<ul><li><strong>Land and access:</strong> Confirm setbacks, easements, slope, soil conditions, road access, turning space, and any delivery restrictions.</li><li><strong>Site preparation:</strong> Ask who handles clearing, grading, drainage, foundation design, and inspections.</li><li><strong>Delivery and setting:</strong> Request a route and access review, a description of setting equipment, and a clear list of delivery-day responsibilities.</li><li><strong>Utilities and completion:</strong> Confirm connection points, service capacity, local trades, interior or exterior completion, and final inspection requirements.</li><li><strong>Contingency:</strong> Keep a realistic allowance for discoveries on the property and changes required by local review.</li></ul>
<p>For a starting point, browse the <a href="/homes-for-sale/">homes and housing options Martin Boxabl showcases</a>, then use the <a href="/gallery/">home design gallery</a> to compare visual approaches. Listings and product details can change, so confirm current specifications and availability directly before making a decision.</p>
<h2>Think about schedule in stages</h2>
<p>Factory production can happen alongside some site work, but that does not remove the time needed for design decisions, financing, approvals, engineering, site preparation, transport coordination, and inspections. Ask for a project schedule that names each stage, the person responsible, the dependencies, and the events that could move the date. Compare that with a site-built schedule based on a similarly complete scope.</p>
<h2>Evaluate design and future use</h2>
<p>Review the actual floor plan, storage, daylight, privacy, accessibility, heating and cooling approach, maintenance needs, and options for future changes. Ask which finishes and fixtures are standard and which cost extra. If you need a particular room arrangement or expansion path, get that answer in writing rather than relying on a rendering.</p>
<h2>Questions to ask before choosing</h2>
<ul><li>What exactly is included in the quoted price, and what is excluded?</li><li>Which local permits, approvals, and inspections are required for this model and parcel?</li><li>Who is responsible for foundation design, utility connections, transport, setting, and finish work?</li><li>What site conditions could prevent delivery or require additional work?</li><li>What warranty applies to the home and to work completed by local contractors?</li><li>Can I review the plans, specifications, code documentation, and contract before paying a deposit?</li></ul>
<p>There is no universal winner between modular and traditional construction. A modular home may suit a buyer who values factory-built components and a defined product specification; a site-built project may suit someone who needs a highly individualized design or has a local team already in place. The useful comparison is a complete, locally reviewed project plan.</p>
<p>Ready to discuss your options? <a href="/contact/">Contact Martin Boxabl</a> with your location, intended use, and questions. For background on the company, visit <a href="/about/">About Martin Boxabl</a>.</p>
""",
    },
    {
        "title": "Modular Home Site Preparation: A Practical Buyer Checklist",
        "slug": "modular-home-site-preparation-checklist",
        "seo_title": "Modular Home Site Preparation Checklist for Buyers",
        "search_description": "Prepare for a modular home with a practical checklist for zoning, surveys, access, soil, foundation, utilities, drainage, permits, and delivery.",
        "excerpt": "A successful modular home project starts with the property. Use this checklist to organize the local approvals, site information, access, foundation, utilities, and delivery questions to resolve before ordering.",
        "category": "Planning & Site Preparation",
        "tags": ["site preparation", "land planning", "modular home foundation", "permits"],
        "image": "static/images/pages/about-home.jpg",
        "image_title": "Modular home site preparation and crane placement",
        "body": """
<p>The parcel can determine whether a home can be placed, how it must be engineered, and what work is needed before delivery. Site preparation is not one task: it is a sequence of local reviews, measurements, design decisions, construction, and inspections. Starting these conversations early can help prevent a finished home from arriving before the site is ready.</p>
<p>Requirements differ by address and by product. Treat this as an organizing checklist, not a substitute for written guidance from your planning office, building department, engineer, utility providers, and the home supplier.</p>
<h2>1. Confirm the intended use is allowed</h2>
<p>Contact the local planning or zoning office with the parcel address and the proposed home type. Ask about permitted use, minimum lot size, setbacks, height limits, density, accessory-unit rules, and any neighborhood or historic restrictions. Verify whether the home will be treated as a permanent dwelling, accessory dwelling, temporary structure, or another category in that jurisdiction.</p>
<p>Ask which documents the authority needs to determine eligibility. A product brochure alone may not be enough; site plans, dimensions, foundation details, engineering, and construction-code documentation may be requested.</p>
<h2>2. Get reliable information about the property</h2>
<p>Locate a current boundary survey and identify easements, rights of way, utility corridors, and property lines. Check the parcel’s slope, drainage patterns, vegetation, and neighboring structures. If the property has not been evaluated for building, ask a qualified local professional whether a geotechnical or soil investigation is appropriate.</p>
<p>Flood exposure, wildfire risk, wind or snow design criteria, and environmental constraints may affect engineering and insurance. Ask the relevant local authority or professional what applies at this address rather than assuming a generic specification will be accepted.</p>
<h2>3. Check the delivery route and the installation area</h2>
<p>A home may fit on the parcel but still be difficult to deliver. Ask the supplier for transport dimensions, turning needs, overhead clearance, weight, and the equipment used for unloading or setting. Walk the route with the delivery team or a qualified logistics provider. Check narrow roads, bridges, low branches and wires, gates, steep grades, soft ground, and space for trucks and lifting equipment.</p>
<p>Identify a staging area and confirm who is responsible for temporary traffic control, road permissions, access repairs, and protecting existing landscaping. The <a href="/gallery/">Martin Boxabl gallery</a> shows examples of home designs, but delivery requirements must be confirmed for the exact model and site.</p>
<h2>4. Coordinate foundation, drainage, and utilities</h2>
<p>Have the foundation designed for the home and local conditions by the appropriate licensed professional. Confirm dimensions, bearing requirements, anchoring, inspections, and how the home will connect to the foundation. Do not assume that a generic slab or a foundation used for another model is suitable.</p>
<p>Map water, sewer or septic, electricity, communications, and any fuel or other services. Verify availability, capacity, connection points, fees, lead times, and trenching responsibilities with each provider. Plan surface drainage so water is directed away from the home and neighboring property in accordance with local requirements.</p>
<h2>5. Build a permit and responsibility tracker</h2>
<p>Make a simple list of each approval, the agency or professional responsible, documents required, submission date, review time, fees, and inspection hold points. Include zoning, building, foundation, utility, driveway or access, stormwater, septic, and environmental reviews if they apply. Ask the supplier which plans and certifications it will provide and what must be prepared locally.</p>
<p>Put responsibilities into the project agreement. Name who obtains each permit, hires each trade, pays each fee, arranges inspections, and resolves corrections. This is especially important when the home supplier, transporter, site contractor, and utility companies are separate organizations.</p>
<h2>Before you place an order</h2>
<ul><li>Confirm the specific model and dimensions fit the parcel’s zoning and setbacks.</li><li>Obtain written feedback from the local building authority on required plans and approvals.</li><li>Review a survey, access route, site conditions, and preliminary foundation approach.</li><li>Get utility availability and connection costs from the providers.</li><li>Agree on a delivery plan, site-readiness criteria, and what happens if the site is not ready.</li><li>Compare a complete project budget, including contingency and local professional fees.</li></ul>
<p>Explore the <a href="/homes-for-sale/home-types/">home types page</a> and <a href="/homes-for-sale/home-categories/">home categories</a> as you narrow the design, then ask the supplier for specifications to share with your local professionals. If you are still at the research stage, the <a href="/homes-for-sale/">homes page</a> outlines the buying process.</p>
<p>When you are ready to talk through next steps, <a href="/contact/">send Martin Boxabl your questions</a> and include the state or region where you plan to build. A location helps make the initial conversation more useful.</p>
""",
    },
    {
        "title": "From Delivery to Move-In: How Modular Home Installation Works",
        "slug": "modular-home-delivery-installation-process",
        "seo_title": "Modular Home Delivery and Installation: What to Expect",
        "search_description": "Learn the usual stages of modular home delivery and installation, from site readiness and transport planning to setting, utility connections, and inspections.",
        "excerpt": "Delivery day is one milestone in a larger project. Understand the usual handoffs between site preparation, transport, setting, utility work, finishing, and local inspections.",
        "category": "Planning & Site Preparation",
        "tags": ["modular home delivery", "installation", "site work", "home buying"],
        "image": "static/images/gallery/gallery-7.jpg",
        "image_title": "Modular home lifted into place during installation",
        "body": """
<p>Seeing a home arrive at its site is an exciting milestone, but delivery is not the same as move-in. A successful project depends on the home, land, transport plan, foundation, utilities, local inspections, and completion work coming together in the right order.</p>
<p>The exact process varies by manufacturer, model, contract, and location. Use the stages below to ask better questions and make sure each handoff has a named owner.</p>
<h2>Stage 1: Confirm the home and project scope</h2>
<p>Before scheduling production or delivery, verify the model, configuration, dimensions, finish choices, included equipment, and written exclusions. Ask what arrives factory-complete and which parts will be finished by local contractors. Confirm the applicable construction documentation and warranty terms for the exact home.</p>
<p>Review the purchase agreement for payment milestones, changes, delivery assumptions, storage or delay costs, and what happens if access or site readiness is not approved. Keep the final plan set and contact list accessible to the supplier, site contractor, transporter, and local authorities.</p>
<h2>Stage 2: Prepare and approve the site</h2>
<p>Complete surveys, engineering, permits, grading, drainage, foundation work, and any required inspections before the scheduled delivery window. Confirm utility routes and connection points. Ask the supplier or installer to provide written site-readiness criteria and schedule a pre-delivery review if one is available.</p>
<p>Verify that the driveway, staging area, and setting area can handle the expected vehicles and equipment. Remove obstacles only after confirming property boundaries and utility locations. A site that is technically buildable may still need additional access work for transport.</p>
<h2>Stage 3: Plan the route and delivery day</h2>
<p>The delivery team should review vehicle dimensions, route restrictions, turning clearances, overhead wires, road conditions, bridge limits, and any permits or escorts required. Confirm the delivery date, weather contingency, unloading method, crew responsibilities, and a contact who can make decisions on site.</p>
<p>Ask what must be clear on the property and who will manage public-road coordination. Keep neighbors informed where access or temporary traffic control may affect them. The supplier should confirm that the route and setting approach work for the specific home, not simply for a similar project elsewhere.</p>
<h2>Stage 4: Set the home and complete connections</h2>
<p>Depending on the design, a crane or other setting equipment may place the home or its sections on the prepared foundation. The crew aligns and secures the structure according to the approved plans. After placement, qualified trades complete the connections and finishing work assigned to them by the contract.</p>
<p>That work may include joining sections, weatherproofing, stairs or access, utility connections, interior or exterior finishes, and commissioning of equipment. Ask which items are part of the supplier’s scope and which belong to the local contractor. Do not treat a visual placement as proof that every system is connected or approved for occupancy.</p>
<h2>Stage 5: Complete inspections and handover</h2>
<p>Arrange required inspections with the local authority and utility providers. Resolve any corrections, collect certificates and warranty documents, review operating instructions, and make a final walkthrough with the responsible parties. Confirm the process for reporting defects and the contact for post-installation questions.</p>
<p>Before move-in, verify that utilities are active, safety systems are working, access is complete, and the approvals required for occupancy have been issued. Keep copies of the approved plans, permits, inspection records, product documentation, and contractor invoices with your home records.</p>
<h2>A practical delivery-day checklist</h2>
<ul><li>The foundation and access are signed off as ready by the responsible professionals.</li><li>Delivery route, permits, equipment, schedule, and weather contingency are confirmed.</li><li>Supplier, installer, transporter, site contractor, and owner responsibilities are clear.</li><li>Utility connections and required inspections are scheduled with the right parties.</li><li>There is a written plan for delays, damage, missing items, and unfinished work.</li></ul>
<p>Martin Boxabl’s <a href="/homes-for-sale/">home buying page</a> describes the broader path from browsing to delivery, while the <a href="/gallery/">gallery</a> offers a look at home designs. For a project-specific conversation, <a href="/contact/">contact Martin Boxabl</a> and ask which delivery and completion responsibilities apply to the model you are considering.</p>
""",
    },
    {
        "title": "How to Choose a Modular Home Floor Plan for Your Lifestyle",
        "slug": "choose-modular-home-floor-plan",
        "seo_title": "How to Choose the Right Modular Home Floor Plan",
        "search_description": "Choose a modular home floor plan by mapping daily routines, room priorities, storage, privacy, accessibility, site limits, and future needs.",
        "excerpt": "The best floor plan is the one that supports your routines and fits your site. Use this practical framework to compare rooms, circulation, storage, privacy, accessibility, and future flexibility.",
        "category": "Design & Floor Plans",
        "tags": ["modular home floor plans", "home design", "small home layouts", "housing options"],
        "image": "static/images/homes/home-1.jpg",
        "image_title": "Modern modular home interior and open living layout",
        "body": """
<p>A floor plan is a daily-use tool, not just a drawing. It determines how people move through the home, where belongings fit, how private rooms feel, and whether shared spaces work for ordinary routines. A thoughtful comparison starts with the way you plan to live, then checks that the design can be approved and placed on your site.</p>
<h2>Start with a typical day</h2>
<p>Write down what happens on a weekday and a weekend: who wakes first, where meals are prepared, whether anyone works or studies at home, where visitors sleep, and what needs to be stored near the entrance. Consider pets, caregiving, hobbies, and equipment. These patterns reveal whether you need a larger shared area, more separation, a second bathroom, or a dedicated room.</p>
<p>Rank needs as essential, preferred, or optional. A clear priority list helps when two plans offer different trade-offs and keeps attractive finishes from distracting from the underlying layout.</p>
<h2>Look beyond the room count</h2>
<p>Two plans with the same number of bedrooms can feel very different. Look at room dimensions, door swings, hallway space, furniture placement, window locations, and the relationship between kitchen, dining, and living areas. Check whether there is enough storage for coats, cleaning supplies, linens, pantry items, and seasonal belongings.</p>
<p>Think about sound and privacy. A bedroom beside a busy living area may not suit shift workers or guests. A bathroom that opens directly into a common space may be less convenient for a household with visitors. If the plan includes a flexible room, identify what it needs to support now and later.</p>
<h2>Plan for comfort and access</h2>
<p>Consider daylight, views, cross-ventilation where relevant, and how the home will be oriented on the parcel. Ask how the home’s heating, cooling, ventilation, and insulation are specified for your climate. Confirm the product documentation rather than assuming that a layout or rendering guarantees a particular performance level.</p>
<p>If accessibility matters now or may matter in the future, ask about step-free entry, clear door openings, turning space, bathroom configuration, reachable storage, and the feasibility of modifications. Get measurements and written confirmation for the specific model.</p>
<h2>Match the plan to the property</h2>
<p>Check the home’s footprint against setbacks, easements, access, orientation, drainage, and the foundation concept. A plan that looks ideal online may not fit the buildable area or the route required to deliver it. Ask whether the layout can be mirrored, rotated, or modified and whether those changes affect engineering, price, or approval.</p>
<p>Browse the <a href="/homes-for-sale/home-types/">home types</a> and <a href="/homes-for-sale/home-categories/">home categories</a> to understand the options Martin Boxabl presents. The <a href="/gallery/">design gallery</a> can help you identify visual preferences, but request dimensioned plans and specifications before comparing exact room sizes.</p>
<h2>Use a consistent comparison sheet</h2>
<p>For each plan, note the usable area, room dimensions, storage, bathrooms, circulation, windows, included appliances, accessibility features, energy systems, customization choices, and total project scope. Record unanswered questions next to the supplier responsible for answering them. This makes a like-for-like comparison much easier.</p>
<ul><li>Does the plan fit your daily routines and furniture?</li><li>Are privacy and noise separation adequate?</li><li>Is there enough storage in the places you need it?</li><li>Can the plan fit the site and delivery route?</li><li>Which features are standard, optional, or unavailable?</li><li>What changes require engineering or additional approval?</li></ul>
<h2>Picture the next five years</h2>
<p>Your needs may change. Consider remote work, a growing or shrinking household, guests, aging in place, or changing mobility. Choose flexibility where it has real value, while remembering that future additions or alterations may require permission and may not be possible for every product.</p>
<p>A useful plan is one that balances comfort, buildability, cost, and maintainability. Start with your priorities, verify dimensions and specifications, and ask how each option fits the property. When you are ready to compare a specific home, <a href="/homes-for-sale/">review the current home options</a> and <a href="/contact/">contact Martin Boxabl</a> with your questions. You can also learn more about the company on the <a href="/about/">About page</a>.</p>
""",
    },
]


class Command(BaseCommand):
    help = "Create or refresh four published Martin Boxabl blog guides."

    @transaction.atomic
    def handle(self, *args, **options):
        root = Page.get_first_root_node()
        if root is None:
            raise CommandError("Wagtail has no root page. Run the site migrations first.")

        index = BlogIndexPage.objects.order_by("path").first()
        if index is None:
            index = BlogIndexPage(
                title="Martin Boxabl Blog",
                slug="blog",
                seo_title="Martin Boxabl Blog | Modular Home Guides",
                search_description="Practical guides to modular homes, site preparation, delivery, and home design.",
                intro="Practical guides to help you compare modern housing options and plan your next steps.",
            )
            root.add_child(instance=index)
            index.save_revision().publish()
            self.stdout.write("Created the blog index page.")
        elif not index.live:
            index.save_revision().publish()

        for data in POSTS:
            image = self._get_image(data)
            category, _ = BlogCategory.objects.get_or_create(name=data["category"])
            page = BlogPostPage.objects.filter(slug=data["slug"]).first()
            is_new = page is None
            if is_new:
                page = BlogPostPage(slug=data["slug"])

            page.title = data["title"]
            page.seo_title = data["seo_title"]
            page.search_description = data["search_description"]
            page.excerpt = data["excerpt"]
            page.body = data["body"].strip()
            page.featured_image = image
            page.category = category
            page.author = "Martin Boxabl"
            page.show_in_menus = False

            if is_new:
                index.add_child(instance=page)
            else:
                page.save()

            page.tags.set(data["tags"])
            page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS(f"Published: {page.title} ({page.url})"))

        self.stdout.write(self.style.SUCCESS("All four blog posts are live and ready for the home page."))

    def _get_image(self, data):
        image_path = Path(__file__).resolve().parents[3] / data["image"]
        if not image_path.is_file():
            raise CommandError(f"Blog image is missing from the deployment: {data['image']}")

        image = Image.objects.filter(title=data["image_title"]).first()
        if image is None:
            with image_path.open("rb") as source:
                image = Image(title=data["image_title"], file=File(source, name=image_path.name))
                image.description = data["image_title"]
                image.save()
        return image
