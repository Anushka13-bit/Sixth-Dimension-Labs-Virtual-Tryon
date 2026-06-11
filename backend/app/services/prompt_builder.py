"""
prompt_builder.py  –  NanaBanana 2 (Gemini multimodal editor) jewellery try-on
================================================================================

HOW NANABANANA 2 WORKS
-----------------------
- It receives TWO images simultaneously in image_urls[]
- image_urls[0] = the person  →  referenced as "the person in the first image"
- image_urls[1] = jewellery   →  referenced as "the jewellery in the second image"
- It understands full natural-language sentences, NOT keyword lists
- There is NO negative_prompt parameter — preservation is written into the prompt

PROMPT STRUCTURE
----------------
1. ROLE ASSIGNMENT   — tell the model what each image is
2. ACTION            — what to place and where
3. JEWELLERY FIDELITY — copy it exactly from image 2, don't redesign
4. IDENTITY LOCK     — everything else about image 1 stays unchanged
5. REALISM           — natural lighting and shadows
"""

from __future__ import annotations


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
    """
    Builds a natural-language prompt for NanaBanana 2.

    The model receives image_urls[0]=person, image_urls[1]=jewellery.
    The prompt references them explicitly so the model knows which to copy
    and which to preserve.
    """
    place = _placement(jewelry_type, user_image_type)

    # Jewellery descriptor — only add fields that aren't already in the name
    desc: list[str] = []
    if jewelry_color and jewelry_color.split()[-1].lower() not in jewelry_name.lower():
        desc.append(jewelry_color)
    if jewelry_material and jewelry_material.split()[-1].lower() not in jewelry_name.lower():
        desc.append(jewelry_material)
    if jewelry_style:
        desc.append(jewelry_style)
    desc.append(jewelry_name)
    jewellery_desc = " ".join(desc)

    # What must stay the same
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

    # Jewellery fidelity — fix "same the same" duplication by using
    # concrete values or falling back to "as shown" instead of "the same X"
    fidelity_parts = [
        "Copy the jewellery from the second image faithfully: same exact shape",
    ]
    if jewelry_material:
        fidelity_parts.append(f"same {jewelry_material}")
    else:
        fidelity_parts.append("same metal and finish as shown")

    if jewelry_color:
        fidelity_parts.append(f"same {jewelry_color} color")
    else:
        fidelity_parts.append("same color and finish as shown")

    fidelity_parts.append("same stone cut and size as shown")
    fidelity_parts.append("Do not simplify, redesign, or add extra stones or elements.")

    # Join first part with commas, last sentence separate
    fidelity = ", ".join(fidelity_parts[:-1]) + ". " + fidelity_parts[-1]

    prompt = (
        f"The first image shows a person. "
        f"The second image shows a {jewellery_desc}. "
        f"Place the {jewellery_desc} from the second image {place} on the person from the first image. "
        f"{fidelity} "
        f"{lock} "
        f"The jewellery should cast a natural shadow and reflect the existing lighting — "
        f"it must look like it was always being worn, not composited on top."
    )
    return prompt.strip()


def build_negative_prompt(user_image_type: str = "face") -> str:
    # NanaBanana has no negative_prompt param — preserved for API compatibility only
    return ""


def build_prompt_with_context(
    jewelry_type: str,
    jewelry_name: str,
    user_image_type: str,
    jewelry_material: str = "",
    jewelry_color: str = "",
    jewelry_style: str = "",
) -> dict[str, str]:
    """
    Returns {"prompt": "...", "negative_prompt": ""}
    negative_prompt is always empty — NanaBanana doesn't support it.
    """
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


if __name__ == "__main__":
    cases = [
        dict(jewelry_type="pendant",  jewelry_name="square emerald solitaire pendant",
             user_image_type="face",  jewelry_material="sterling silver", jewelry_color="green emerald"),
        dict(jewelry_type="earrings", jewelry_name="gold jhumka",
             user_image_type="face",  jewelry_material="22k gold", jewelry_style="traditional"),
        dict(jewelry_type="ring",     jewelry_name="diamond solitaire ring",
             user_image_type="hand",  jewelry_material="platinum"),
        dict(jewelry_type="necklace", jewelry_name="Emerald Necklace",
             user_image_type="face"),
    ]
    for c in cases:
        r = build_prompt_with_context(**c)
        print(f"\n{'='*60}")
        print(f"TYPE: {c['jewelry_type']} / {c['user_image_type']}")
        print(f"PROMPT:\n{r['prompt']}")