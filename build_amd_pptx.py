from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt


OUTPUT_PATH = Path("/workspace/amd-presentation-draft.pptx")

BACKGROUND = RGBColor(15, 23, 42)
PANEL = RGBColor(17, 24, 39)
ACCENT = RGBColor(249, 115, 22)
ACCENT_LIGHT = RGBColor(253, 186, 116)
TEXT = RGBColor(229, 231, 235)
MUTED = RGBColor(148, 163, 184)
WHITE = RGBColor(255, 255, 255)


def set_background(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = BACKGROUND


def add_header(slide, title, kicker=None):
    if kicker:
        kicker_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(4.0), Inches(0.3))
        frame = kicker_box.text_frame
        frame.clear()
        p = frame.paragraphs[0]
        run = p.add_run()
        run.text = kicker.upper()
        run.font.name = "Arial"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = ACCENT_LIGHT

    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.65), Inches(11.6), Inches(0.7))
    frame = title_box.text_frame
    frame.clear()
    frame.word_wrap = True
    p = frame.paragraphs[0]
    run = p.add_run()
    run.text = title
    run.font.name = "Arial"
    run.font.size = Pt(26)
    run.font.bold = True
    run.font.color.rgb = WHITE

    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.42), Inches(2.2), Inches(0.08))
    accent.fill.solid()
    accent.fill.fore_color.rgb = ACCENT
    accent.line.fill.background()


def add_footer(slide, slide_number):
    footer_box = slide.shapes.add_textbox(Inches(0.6), Inches(6.95), Inches(12.0), Inches(0.25))
    frame = footer_box.text_frame
    frame.clear()
    p = frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    run = p.add_run()
    run.text = f"AMD draft deck | Slide {slide_number}"
    run.font.name = "Arial"
    run.font.size = Pt(10)
    run.font.color.rgb = MUTED


def add_panel(slide, left, top, width, height, title=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = PANEL
    shape.line.color.rgb = RGBColor(51, 65, 85)
    shape.line.width = Pt(1.0)
    shape.adjustments[0] = 0.08

    if title:
        title_box = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.12), width - Inches(0.36), Inches(0.3))
        frame = title_box.text_frame
        frame.clear()
        p = frame.paragraphs[0]
        run = p.add_run()
        run.text = title
        run.font.name = "Arial"
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = ACCENT_LIGHT

    return shape


def add_bullets(slide, left, top, width, height, bullets, font_size=20, level_step=0):
    box = slide.shapes.add_textbox(left, top, width, height)
    frame = box.text_frame
    frame.word_wrap = True
    frame.auto_size = MSO_AUTO_SIZE.NONE
    frame.clear()

    for idx, item in enumerate(bullets):
        if isinstance(item, tuple):
            level, text = item
        else:
            level, text = level_step, item
        p = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
        p.level = level
        p.space_after = Pt(6)
        p.bullet = True
        run = p.add_run()
        run.text = text
        run.font.name = "Arial"
        run.font.size = Pt(font_size - level * 2)
        run.font.color.rgb = TEXT


def add_metric(slide, left, top, width, height, value, label):
    add_panel(slide, left, top, width, height)
    value_box = slide.shapes.add_textbox(left + Inches(0.16), top + Inches(0.16), width - Inches(0.32), Inches(0.5))
    frame = value_box.text_frame
    p = frame.paragraphs[0]
    run = p.add_run()
    run.text = value
    run.font.name = "Arial"
    run.font.size = Pt(24)
    run.font.bold = True
    run.font.color.rgb = WHITE

    label_box = slide.shapes.add_textbox(left + Inches(0.16), top + Inches(0.72), width - Inches(0.32), height - Inches(0.88))
    frame = label_box.text_frame
    frame.word_wrap = True
    p = frame.paragraphs[0]
    run = p.add_run()
    run.text = label
    run.font.name = "Arial"
    run.font.size = Pt(12)
    run.font.color.rgb = MUTED


def title_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)

    add_panel(slide, Inches(0.55), Inches(0.45), Inches(12.2), Inches(6.2))

    title_box = slide.shapes.add_textbox(Inches(0.95), Inches(1.0), Inches(8.3), Inches(1.1))
    frame = title_box.text_frame
    frame.clear()
    p = frame.paragraphs[0]
    run = p.add_run()
    run.text = "Acid Mine Drainage (AMD)"
    run.font.name = "Arial"
    run.font.size = Pt(30)
    run.font.bold = True
    run.font.color.rgb = WHITE

    subtitle_box = slide.shapes.add_textbox(Inches(0.95), Inches(2.0), Inches(8.7), Inches(1.2))
    frame = subtitle_box.text_frame
    frame.clear()
    p = frame.paragraphs[0]
    run = p.add_run()
    run.text = (
        "Draft presentation covering environmental risk, energy supply chain impacts, "
        "treatment technologies, economics, regulation, and case studies."
    )
    run.font.name = "Arial"
    run.font.size = Pt(19)
    run.font.color.rgb = TEXT

    topic_box = slide.shapes.add_textbox(Inches(0.95), Inches(3.35), Inches(10.8), Inches(1.6))
    frame = topic_box.text_frame
    frame.word_wrap = True
    frame.clear()
    for idx, text in enumerate(
        [
            "Energy supply chain",
            "Technology approaches",
            "Economics / costs / financing",
            "Laws and regulations",
            "Example cases",
        ]
    ):
        p = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
        run = p.add_run()
        run.text = text
        run.font.name = "Arial"
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = ACCENT_LIGHT
        p.space_after = Pt(10)

    message_box = slide.shapes.add_textbox(Inches(8.7), Inches(1.0), Inches(3.1), Inches(4.3))
    frame = message_box.text_frame
    frame.word_wrap = True
    frame.clear()
    p = frame.paragraphs[0]
    run = p.add_run()
    run.text = (
        "Key message:\nAMD is both a long-tail water liability and an emerging "
        "critical-minerals recovery opportunity."
    )
    run.font.name = "Arial"
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = WHITE

    chem_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.55), Inches(4.9), Inches(3.35), Inches(1.0))
    chem_box.fill.solid()
    chem_box.fill.fore_color.rgb = RGBColor(48, 23, 9)
    chem_box.line.color.rgb = ACCENT
    chem_text = slide.shapes.add_textbox(Inches(8.72), Inches(5.14), Inches(3.05), Inches(0.5))
    frame = chem_text.text_frame
    p = frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = "2FeS2 + 7O2 + 2H2O -> 2Fe2+ + 4SO4^2- + 4H+"
    run.font.name = "Courier New"
    run.font.size = Pt(13)
    run.font.color.rgb = WHITE

    add_footer(slide, 1)


def bullet_slide(prs, number, kicker, title, bullets, source_text=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_header(slide, title, kicker)
    add_panel(slide, Inches(0.6), Inches(1.7), Inches(12.1), Inches(4.95))
    add_bullets(slide, Inches(0.9), Inches(2.0), Inches(11.4), Inches(4.4), bullets, font_size=20)
    if source_text:
        src = slide.shapes.add_textbox(Inches(0.85), Inches(6.45), Inches(8.0), Inches(0.25))
        frame = src.text_frame
        p = frame.paragraphs[0]
        run = p.add_run()
        run.text = source_text
        run.font.name = "Arial"
        run.font.size = Pt(10)
        run.font.color.rgb = MUTED
    add_footer(slide, number)


def technology_slide(prs, number):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_header(slide, "Technology approaches: predict, prevent, treat, and recover", "Technology")

    panels = [
        (Inches(0.6), Inches(1.8), Inches(2.9), Inches(2.0), "Prediction",
         ["Static/kinetic testing", "Geochemical modeling", "Waste characterization"]),
        (Inches(3.75), Inches(1.8), Inches(2.9), Inches(2.0), "Prevention",
         ["Covers and encapsulation", "Water diversion", "Alkaline blending / backfilling"]),
        (Inches(6.9), Inches(1.8), Inches(2.9), Inches(2.0), "Active treatment",
         ["Lime or caustic neutralization", "Aeration and sludge handling", "Best for high flow and variable chemistry"]),
        (Inches(10.05), Inches(1.8), Inches(2.65), Inches(2.0), "Passive treatment",
         ["ALDs, SAPS, wetlands", "Lower O&M", "Needs land and site-specific chemistry"]),
        (Inches(1.9), Inches(4.15), Inches(4.2), Inches(1.8), "Recovery / reuse",
         ["Recover rare earths or cobalt from AMD solids where enriched", "Potential cost offset, but still site-specific and emerging"]),
        (Inches(6.45), Inches(4.15), Inches(4.2), Inches(1.8), "Practical lesson",
         ["Most successful projects combine source control with active or passive polishing rather than using a single method alone"]),
    ]

    for left, top, width, height, title, bullets in panels:
        add_panel(slide, left, top, width, height, title=title)
        add_bullets(slide, left + Inches(0.15), top + Inches(0.48), width - Inches(0.3), height - Inches(0.56), bullets, font_size=13)

    src = slide.shapes.add_textbox(Inches(0.85), Inches(6.45), Inches(8.5), Inches(0.25))
    frame = src.text_frame
    p = frame.paragraphs[0]
    run = p.add_run()
    run.text = "Sources: EPA MIW treatment guide; EPA AMD overview; NETL / OSTI summaries."
    run.font.name = "Arial"
    run.font.size = Pt(10)
    run.font.color.rgb = MUTED
    add_footer(slide, number)


def economics_slide(prs, number):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_header(slide, "Economics, costs, and financing", "Economics")

    add_metric(slide, Inches(0.75), Inches(1.85), Inches(3.7), Inches(1.5), "$34 / ton", "EPA example cost for in situ limestone drain acid-load treatment.")
    add_metric(slide, Inches(4.85), Inches(1.85), Inches(3.2), Inches(1.5), "$441 / ton", "Comparable conventional caustic soda treatment cost in the same example.")
    add_metric(slide, Inches(8.45), Inches(1.85), Inches(3.5), Inches(1.5), "$5,700 / km / year", "Estimated stream-protection cost from Pennsylvania treatment-system analysis.")

    add_panel(slide, Inches(0.75), Inches(3.7), Inches(5.65), Inches(2.45), "Cost drivers")
    add_bullets(
        slide,
        Inches(0.95),
        Inches(4.15),
        Inches(5.25),
        Inches(1.8),
        [
            "Active systems trade reliability for recurring energy, chemical, labor, and sludge costs.",
            "Passive systems lower O&M but need land, maintenance, and favorable geochemistry.",
            "Bonding and financial assurance must account for long-term post-closure water treatment.",
        ],
        font_size=15,
    )

    add_panel(slide, Inches(6.75), Inches(3.7), Inches(5.2), Inches(2.45), "Financing implication")
    add_bullets(
        slide,
        Inches(6.95),
        Inches(4.15),
        Inches(4.8),
        Inches(1.8),
        [
            "AMD is often a decades-long liability rather than a one-time capex item.",
            "Public AML funds frequently fill abandoned-site gaps.",
            "Critical-mineral recovery is promising as an offset, but should not be the only funding assumption.",
        ],
        font_size=15,
    )

    src = slide.shapes.add_textbox(Inches(0.85), Inches(6.45), Inches(10.0), Inches(0.25))
    frame = src.text_frame
    p = frame.paragraphs[0]
    run = p.add_run()
    run.text = "Sources: EPA SBIR limestone-drain example; Communications Earth & Environment (2024); EPA MIW treatment guide."
    run.font.name = "Arial"
    run.font.size = Pt(10)
    run.font.color.rgb = MUTED
    add_footer(slide, number)


def regulations_slide(prs, number):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_header(slide, "Laws and regulations", "Regulation")

    add_panel(slide, Inches(0.75), Inches(1.85), Inches(5.8), Inches(4.9), "United States")
    add_bullets(
        slide,
        Inches(1.0),
        Inches(2.3),
        Inches(5.3),
        Inches(4.1),
        [
            "Clean Water Act / NPDES permits regulate mine-water discharges.",
            "40 CFR Part 434 covers acid or ferruginous mine drainage and related coal-mining subcategories.",
            "Illustrative new-source limits: total iron 6.0 mg/L daily max, 3.0 mg/L 30-day average; manganese 4.0 / 2.0; TSS 70 / 35; pH 6.0-9.0.",
            "SMCRA and abandoned mine land programs support reclamation and AMD abatement.",
            "CERCLA / Superfund applies at major contaminated legacy sites.",
        ],
        font_size=15,
    )

    add_panel(slide, Inches(6.8), Inches(1.85), Inches(5.2), Inches(4.9), "European Union / international")
    add_bullets(
        slide,
        Inches(7.05),
        Inches(2.3),
        Inches(4.7),
        Inches(4.1),
        [
            "EU Extractive Waste Directive (2006/21/EC) requires waste-management plans, permits, closure plans, monitoring, and pollution prevention.",
            "The Water Framework Directive adds protection against deterioration of receiving-water status.",
            "Across jurisdictions, the trend is toward stronger closure planning, more monitoring, and clearer polluter-pays obligations.",
        ],
        font_size=15,
    )

    src = slide.shapes.add_textbox(Inches(0.85), Inches(6.45), Inches(10.0), Inches(0.25))
    frame = src.text_frame
    p = frame.paragraphs[0]
    run = p.add_run()
    run.text = "Sources: EPA Coal Mining Effluent Guidelines; eCFR 40 CFR Part 434 and 30 CFR Part 876; EU mining-waste overview."
    run.font.name = "Arial"
    run.font.size = Pt(10)
    run.font.color.rgb = MUTED
    add_footer(slide, number)


def case_grid_slide(prs, number, kicker, title, cards, source_text):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_header(slide, title, kicker)

    positions = [
        (Inches(0.75), Inches(1.85)),
        (Inches(4.4), Inches(1.85)),
        (Inches(8.05), Inches(1.85)),
    ]
    width = Inches(3.25)
    height = Inches(4.95)

    for (left, top), (card_title, bullets) in zip(positions, cards):
        add_panel(slide, left, top, width, height, title=card_title)
        add_bullets(slide, left + Inches(0.18), top + Inches(0.48), width - Inches(0.36), height - Inches(0.7), bullets, font_size=15)

    src = slide.shapes.add_textbox(Inches(0.85), Inches(6.45), Inches(10.0), Inches(0.25))
    frame = src.text_frame
    p = frame.paragraphs[0]
    run = p.add_run()
    run.text = source_text
    run.font.name = "Arial"
    run.font.size = Pt(10)
    run.font.color.rgb = MUTED
    add_footer(slide, number)


def final_slide(prs, number):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_header(slide, "Takeaways and export note", "Wrap-up")

    add_panel(slide, Inches(0.75), Inches(1.85), Inches(6.1), Inches(4.8), "Main takeaways")
    add_bullets(
        slide,
        Inches(1.0),
        Inches(2.3),
        Inches(5.6),
        Inches(4.0),
        [
            "AMD is a predictable geochemical risk that should be addressed early in mine design and closure planning.",
            "Source control is usually more durable than relying only on downstream treatment.",
            "For energy and mining supply chains, AMD affects permitting, cost, financing, community acceptance, and ESG risk.",
            "Recovery of rare earths and other critical minerals from AMD solids is promising but still highly site-specific.",
        ],
        font_size=16,
    )

    add_panel(slide, Inches(7.15), Inches(1.85), Inches(4.85), Inches(2.1), "Google Slides import")
    add_bullets(
        slide,
        Inches(7.4),
        Inches(2.3),
        Inches(4.35),
        Inches(1.45),
        [
            "Open Google Slides.",
            "File -> Open -> Upload.",
            "Select amd-presentation-draft.pptx.",
            "Google Slides will convert it into an editable deck.",
        ],
        font_size=15,
    )

    add_panel(slide, Inches(7.15), Inches(4.2), Inches(4.85), Inches(2.45), "Selected references")
    add_bullets(
        slide,
        Inches(7.4),
        Inches(4.65),
        Inches(4.35),
        Inches(1.7),
        [
            "EPA abandoned mine drainage overview",
            "USGS acid mine drainage overview",
            "EPA MIW treatment guide",
            "Black and Weber (2024)",
            "NETL / OSTI REE recovery summaries",
        ],
        font_size=14,
    )

    add_footer(slide, number)


def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    prs.core_properties.title = "Acid Mine Drainage (AMD) Draft Deck"
    prs.core_properties.subject = "AMD presentation for Google Slides import"
    prs.core_properties.author = "OpenAI Cursor Agent"
    prs.core_properties.keywords = "acid mine drainage, AMD, mining, water treatment, google slides"

    title_slide(prs)
    bullet_slide(
        prs,
        2,
        "Overview",
        "What acid mine drainage is",
        [
            "AMD forms when sulfide minerals such as pyrite are exposed to air and water during or after mining.",
            "Oxidation generates sulfuric acid and mobilizes dissolved metals such as iron, aluminum, and manganese.",
            "Microbial activity can accelerate these reactions and make the drainage persist for decades or longer.",
            "AMD can occur at both active and abandoned coal and metal mines.",
        ],
        source_text="Sources: U.S. EPA abandoned mine drainage overview; USGS acid mine drainage overview.",
    )
    bullet_slide(
        prs,
        3,
        "Impact",
        "Why AMD matters",
        [
            "Acidic, metal-rich water degrades streams, groundwater, sediments, aquatic habitat, and downstream water uses.",
            "EPA guidance notes mining-influenced water affects more than 10,000 miles of receiving waters in the United States.",
            "Pennsylvania reports roughly 5,600 AMD-impaired stream miles, showing how severe the issue can become in legacy coal regions.",
            "The problem can outlast mine closure and become a public liability if treatment or maintenance stops.",
        ],
        source_text="Sources: EPA MIW treatment guide; PA AMD impairment summaries; SRBC regional strategy materials.",
    )
    bullet_slide(
        prs,
        4,
        "Supply chain",
        "Energy supply chain implications",
        [
            "AMD is a mining and energy supply-chain issue because water liabilities affect permitting, capital planning, bonding, and long-term operating costs.",
            "Treatment itself becomes part of the supply chain through demand for lime, limestone, power, pumps, labor, and sludge handling.",
            "NETL reports AMD treatment wastes in Appalachia may contain about 1,102 tons per year of rare earth element potential.",
            "That makes AMD both a liability and a possible unconventional feedstock for critical minerals used in advanced energy technologies.",
        ],
        source_text="Sources: NETL Geological and Environmental Systems page; OSTI REE-from-AMD summaries.",
    )
    technology_slide(prs, 5)
    economics_slide(prs, 6)
    regulations_slide(prs, 7)
    case_grid_slide(
        prs,
        8,
        "Case study",
        "Summitville Mine, Colorado",
        [
            ("Problem", ["Open-pit gold mining and heap leaching increased AMD generation in a sulfide-rich setting.", "Acidic, metal-laden drainage damaged aquatic life for more than 20 miles downstream."]),
            ("Response", ["EPA took over operations after bankruptcy and focused on both water treatment and source control.", "Major acid-generating wastes were moved into lined, capped repositories."]),
            ("Lesson", ["Reported treatment cost was about $50,000 per day during response planning.", "Poor AMD control can become a long-term public finance and regulatory problem."]),
        ],
        "Sources: Summitville technical papers and reclamation case documentation.",
    )
    case_grid_slide(
        prs,
        9,
        "Case study",
        "Wheal Jane, Cornwall",
        [
            ("Problem", ["Mine closure and rebound of mine water led to a highly visible acidic discharge into the Carnon River system.", "The site became a flagship AMD remediation case in the UK."]),
            ("Passive pilot", ["Pilot systems used reed beds, aerobic and anaerobic cells, rock filters, and pretreatment options.", "The work showed useful natural attenuation and metal-removal performance."]),
            ("Lesson", ["Passive systems were informative but limited by land, plugging, and flow constraints.", "An active lime plant was still needed to handle the full discharge."]),
        ],
        "Sources: Wheal Jane bioremediation literature and ITRC case-study summary.",
    )
    case_grid_slide(
        prs,
        10,
        "Outlook",
        "Appalachia: restoration plus critical-minerals recovery",
        [
            ("Restoration", ["Decades of Pennsylvania treatment-system data show AMD cleanup can protect streams cost-effectively.", "This makes AMD infrastructure a regional water-restoration tool."]),
            ("Just transition", ["AMD burdens often overlap with communities affected by coal decline and economic transition.", "Cleanup therefore also supports regional redevelopment and public health."]),
            ("Recovery opportunity", ["NETL and partners are developing processes to recover REEs and cobalt from AMD treatment solids.", "This could shift some sites from pure cost centers toward remediation plus materials recovery."]),
        ],
        "Sources: Black and Weber (2024); NETL / OSTI rare-earth recovery work.",
    )
    final_slide(prs, 11)
    prs.save(OUTPUT_PATH)


if __name__ == "__main__":
    build_presentation()
    print(f"Wrote {OUTPUT_PATH}")
