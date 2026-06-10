def build_prompt(jewelry_type: str, jewelry_name: str) -> str:
    placement_rules = {
        "necklace": "Place the necklace naturally around the neck and collarbone area.",
        "earrings": "Place the earrings naturally on the visible ear or both ears if visible.",
        "ring": "Place the ring naturally on an appropriate finger.",
        "bracelet": "Place the bracelet naturally around the wrist.",
        "bangle": "Place the bangle naturally around the wrist.",
        "watch": "Place the watch naturally on the wrist.",
        "pendant": "Place the pendant naturally around the neck.",
        "chain": "Place the chain naturally around the neck.",
        "nose_ring": "Place the nose ring naturally on the nostril.",
        "anklet": "Place the anklet naturally around the ankle."
    }

    placement_instruction = placement_rules.get(
        jewelry_type.lower(),
        f"Place the {jewelry_name} naturally where it would normally be worn."
    )

    prompt = f"""
You are performing a reference-based image editing task.

INPUTS:
- User image = the person image (base image to edit)
- Reference image = {jewelry_name} product image (jewelry only)

TASK:
Transfer the exact jewelry from the reference image onto the user image.

IMPORTANT RULES:
- Edit ONLY the user image.
- Do NOT modify or reinterpret the jewelry design.

PLACEMENT:
{placement_instruction}

PRESERVATION RULES:
- Preserve identity, face, skin texture, body shape, pose, clothing, hairstyle, makeup, and background exactly.
- Preserve jewelry design, metal, gemstones, texture, proportions, and details exactly.

RENDERING RULES:
- Match lighting, shadows, reflections, perspective, and depth.
- Ensure natural occlusion and physical wear.
- Jewelry must look realistically worn on the body.

STRICT CONSTRAINTS:
- No floating jewelry
- No extra jewelry
- No duplicated jewelry
- No body changes
- No background changes
- No edits outside jewelry placement

STYLE:
Photorealistic luxury jewelry try-on photography.
"""

    return prompt.strip()


def build_prompt_with_context(
    jewelry_type: str,
    jewelry_name: str,
    user_image_type: str
) -> str:
    """
    Build a context-aware prompt with region constraints.
    """

    prompt = build_prompt(jewelry_type, jewelry_name)

    context_rules = {
        "face": "Apply jewelry only to the visible face/head region.",
        "ear": "Apply jewelry only to the visible ear region.",
        "neck": "Apply jewelry only to the visible neck/collar region.",
        "hand": "Apply jewelry only to the visible hand/wrist region.",
        "wrist": "Apply jewelry only to the visible wrist region.",
        "finger": "Apply jewelry only to the visible finger region.",
        "upper_body": "Apply jewelry only to the visible upper-body region.",
        "full_body": "Apply jewelry only where it would naturally be worn."
    }

    if user_image_type:
        rule = context_rules.get(user_image_type.lower())
        if rule:
            prompt += f"\n\nREGION CONSTRAINT:\n{rule}"

    return prompt