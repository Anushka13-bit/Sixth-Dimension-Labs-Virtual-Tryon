"""
prompt_builder.py  –  NanaBanana 2 virtual try-on
===================================================
Supports two categories:
  - "jewellery"  : unchanged from working version
  - "apparel"    : new
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# JEWELLERY — exactly as before, untouched
# ---------------------------------------------------------------------------
_PLACEMENT: dict[str, str] = {
    "ring":        "on her ring finger",
    "bracelet":    "around her wrist",
    "bangle":      "around her wrist",
    "necklace":    "around her neck, resting on her chest",
    "pendant":     "around her neck, hanging on her chest",
    "earring":     "on her earlobe",
    "earrings":    "on her earlobes",
    "nose ring":   "on her nostril",
    "nose pin":    "on her nostril",
    "anklet":      "around her ankle",
    "maangtikka":  "along her forehead parting",
    "mangalsutra": "around her neck",
    "chain":       "around her neck",
    "brooch":      "pinned on her clothing near the chest",
    "armlet":      "around her upper arm",
}

_HAND_PLACEMENT: dict[str, str] = {
    "ring":     "on the finger",
    "bracelet": "around the wrist",
    "bangle":   "around the wrist",
    "anklet":   "around the ankle",
    "armlet":   "around the upper arm",
}


def _placement(jewelry_type: str, user_image_type: str) -> str:
    key = jewelry_type.lower().strip()
    if user_image_type == "hand":
        return _HAND_PLACEMENT.get(key, "on the hand")
    return _PLACEMENT.get(key, "on the person")


def build_prompt(
    jewelry_type: str,
    jewelry_name: str,
    user_image_type: str = "face",
    jewelry_material: str = "",
    jewelry_color: str = "",
    jewelry_style: str = "",
) -> str:
    place = _placement(jewelry_type, user_image_type)

    desc: list[str] = []
    if jewelry_color and jewelry_color.split()[-1].lower() not in jewelry_name.lower():
        desc.append(jewelry_color)
    if jewelry_material and jewelry_material.split()[-1].lower() not in jewelry_name.lower():
        desc.append(jewelry_material)
    if jewelry_style:
        desc.append(jewelry_style)
    desc.append(jewelry_name)
    jewellery_desc = " ".join(desc)

    if user_image_type == "face":
        lock = (
            "Keep the person's face, skin tone, eye color, hair, expression, "
            "pose, clothing, and background pixel-perfect — do not alter them at all."
        )
    else:
        lock = (
            "Keep the hand's skin tone, finger shape, nails, pose, and background "
            "exactly as they are — do not change anything about the hand."
        )

    fidelity_parts = ["Copy the jewellery from the second image faithfully: same exact shape"]
    fidelity_parts.append(f"same {jewelry_material}" if jewelry_material else "same metal and finish as shown")
    fidelity_parts.append(f"same {jewelry_color} color" if jewelry_color else "same color and finish as shown")
    fidelity_parts.append("same stone cut and size as shown")
    fidelity = ", ".join(fidelity_parts) + ". Do not simplify, redesign, or add extra stones or elements."

    return (
        f"The first image shows a person. "
        f"The second image shows a {jewellery_desc}. "
        f"Place the {jewellery_desc} from the second image {place} on the person from the first image. "
        f"{fidelity} "
        f"{lock} "
        f"The jewellery should cast a natural shadow and reflect the existing lighting — "
        f"it must look like it was always being worn, not composited on top."
    ).strip()


def build_negative_prompt(user_image_type: str = "face") -> str:
    return ""


def build_prompt_with_context(
    jewelry_type: str,
    jewelry_name: str,
    user_image_type: str,
    jewelry_material: str = "",
    jewelry_color: str = "",
    jewelry_style: str = "",
) -> dict[str, str]:
    return {
        "prompt": build_prompt(
            jewelry_type=jewelry_type,
            jewelry_name=jewelry_name,
            user_image_type=user_image_type,
            jewelry_material=jewelry_material,
            jewelry_color=jewelry_color,
            jewelry_style=jewelry_style,
        ),
        "negative_prompt": "",
    }


# ---------------------------------------------------------------------------
# APPAREL — new addition
# ---------------------------------------------------------------------------
_APPAREL_COVERAGE: dict[str, str] = {
    "shirt":         "the upper body from shoulders to waist",
    "blouse":        "the upper body from shoulders to waist",
    "top":           "the upper body from shoulders to waist",
    "crop top":      "the upper body from shoulders to midriff",
    "t-shirt":       "the upper body from shoulders to waist",
    "kurta":         "the upper body and hips",
    "kurti":         "the upper body and hips",
    "jacket":        "the upper body including arms",
    "blazer":        "the upper body including arms",
    "coat":          "the upper body and arms",
    "hoodie":        "the upper body including arms",
    "sweater":       "the upper body including arms",
    "skirt":         "the lower body from waist to knee or below",
    "pants":         "the lower body from waist to ankle",
    "trousers":      "the lower body from waist to ankle",
    "jeans":         "the lower body from waist to ankle",
    "leggings":      "the lower body from waist to ankle",
    "shorts":        "the lower body from waist to mid-thigh",
    "salwar":        "the lower body from waist to ankle",
    "dress":         "the full body from shoulders to knee or below",
    "gown":          "the full body from shoulders to floor",
    "saree":         "the full body draped from shoulder across the torso to floor",
    "lehenga":       "the full body — fitted blouse on top, flared skirt below",
    "jumpsuit":      "the full body from shoulders to ankle",
    "suit":          "the full body — jacket on top, trousers below",
    "salwar kameez": "the full body — top and trousers",
    "anarkali":      "the full body — fitted bodice with flared floor-length skirt",
    "dupatta":       "draped over one shoulder and across the chest",
    "scarf":         "draped around the neck and shoulders",
}


def build_apparel_prompt(
    apparel_type: str,
    apparel_name: str,
    apparel_material: str = "",
    apparel_color: str = "",
    apparel_fit: str = "",
    apparel_pattern: str = "",
) -> str:
    coverage = _APPAREL_COVERAGE.get(apparel_type.lower().strip(), "the body")
    name_lower = apparel_name.lower()

    # Build descriptor — skip fields whose words are already in the name
    desc: list[str] = []
    if apparel_color and not any(w in name_lower for w in apparel_color.lower().split()):
        desc.append(apparel_color)
    if apparel_material and not any(w in name_lower for w in apparel_material.lower().split()):
        desc.append(apparel_material)
    if apparel_pattern and not any(w in name_lower for w in apparel_pattern.lower().split()):
        desc.append(apparel_pattern)
    if apparel_fit:
        desc.append(apparel_fit)
    desc.append(apparel_name)
    apparel_desc = " ".join(desc)

    # Fidelity — what must match the product image
    fidelity_parts = [f"Copy the {apparel_name} from the second image exactly: same cut and silhouette"]
    fidelity_parts.append(f"same {apparel_color} color" if apparel_color else "same color as shown")
    fidelity_parts.append(f"same {apparel_material} fabric texture" if apparel_material else "same fabric texture as shown")
    if apparel_pattern:
        fidelity_parts.append(f"same {apparel_pattern} — do not alter the print or embroidery")
    if apparel_fit:
        fidelity_parts.append(f"same {apparel_fit} fit")
    fidelity_parts.append("same neckline, sleeve length, and hem length as shown in the second image")
    fidelity = ", ".join(fidelity_parts) + ". Do not change the design, add extra details, or alter the style."

    # Product-photo cleanup — the second image is catalog/product photography and
    # often contains artifacts that are NOT part of the garment itself. These must
    # never be copied onto the person.
    cleanup = (
        "The second image is a product photo, not the garment as actually worn — ignore and exclude "
        "anything that is not the garment fabric itself: price tags, brand tags, size labels, "
        "hangers, mannequin clips or pins, stickers, or any tag or label sewn onto or hanging from the garment. "
        "The final result must show only clean fabric with no tags, labels, or stickers of any kind visible."
    )

    # Preservation — what must NOT change
    lock = (
        "Keep the person's face, skin tone, hair, and expression exactly as they are. "
        "Keep the person's body shape, pose, and proportions unchanged — "
        "do not make the person slimmer, taller, or alter their build. "
        "If the new garment exposes skin that the original clothing covered "
        "(such as arms, shoulders, or midriff), render that skin with the same tone and texture "
        "as the rest of the person's visible skin. "
        "Keep the background exactly as it is."
    )

    # Realism — how the garment should look worn (concrete physical cues,
    # not just "look realistic" — vague realism language gets ignored)
    realism = (
        f"Render the {apparel_name} as if it were physically worn on a real body, not as a flat overlay: "
        f"the fabric must compress and fold at the joints — elbows, waist, where the body bends — "
        f"with visible creases and gathered fabric, not a smooth flat surface. "
        f"The garment must conform to the body's actual contours — following the curve of the chest, "
        f"waist, and torso with subtle fabric tension and stretch, rather than sitting as a flat, "
        f"perfectly smooth panel disconnected from the body underneath. "
        f"Cast a soft contact shadow from the garment onto the body and onto any garment beneath it "
        f"(for example, where a top overlaps the waistband below). "
        f"The fabric's highlights and shadows must follow the same light direction and intensity "
        f"as the skin and background in the first image — match the warmth, contrast, and shadow softness exactly. "
        f"Loose or flowy parts of the garment (sleeves, ties, hems) should respond to gravity, "
        f"hanging and curving naturally rather than appearing stiff or rigid. "
        f"The edges where the garment meets skin should blend naturally with soft shadow transition, "
        f"not a hard cutout line."
    )

    # Replacement instruction — explicit removal of existing clothing
    replacement = (
        f"Completely remove the clothing the person is currently wearing on {coverage} "
        f"and replace it with the {apparel_desc} from the second image. "
        f"None of the original outfit's fabric, color, pattern, or texture should remain visible — "
        f"the new garment fully covers that region as its own layer, not on top of the old one."
    )

    return (
        f"The first image shows a person wearing their own clothes. "
        f"The second image shows a {apparel_desc} on its own. "
        f"{replacement} "
        f"{cleanup} "
        f"{fidelity} "
        f"{lock} "
        f"{realism}"
    ).strip()


def build_apparel_prompt_with_context(
    apparel_type: str,
    apparel_name: str,
    apparel_material: str = "",
    apparel_color: str = "",
    apparel_fit: str = "",
    apparel_pattern: str = "",
) -> dict[str, str]:
    return {
        "prompt": build_apparel_prompt(
            apparel_type=apparel_type,
            apparel_name=apparel_name,
            apparel_material=apparel_material,
            apparel_color=apparel_color,
            apparel_fit=apparel_fit,
            apparel_pattern=apparel_pattern,
        ),
        "negative_prompt": "",
    }


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== JEWELLERY (unchanged) ===")
    r = build_prompt_with_context(
        jewelry_type="pendant",
        jewelry_name="square emerald solitaire pendant",
        user_image_type="face",
        jewelry_material="sterling silver",
        jewelry_color="green emerald",
    )
    print(r["prompt"])

    print("\n=== APPAREL ===")
    cases = [
        dict(apparel_type="saree",   apparel_name="Banarasi silk saree",
             apparel_color="red and gold", apparel_material="silk",
             apparel_pattern="zari embroidery"),
        dict(apparel_type="dress",   apparel_name="floral wrap dress",
             apparel_color="blue",   apparel_material="chiffon",
             apparel_fit="flowy",    apparel_pattern="floral print"),
        dict(apparel_type="kurta",   apparel_name="embroidered cotton kurta",
             apparel_color="white",  apparel_material="cotton",
             apparel_fit="loose",    apparel_pattern="floral embroidery"),
        dict(apparel_type="jacket",  apparel_name="leather biker jacket",
             apparel_color="black",  apparel_material="leather",
             apparel_fit="slim fit"),
    ]
    for c in cases:
        r = build_apparel_prompt_with_context(**c)
        print(f"\n[{c['apparel_type']}] {c['apparel_name']}")
        print(r["prompt"])