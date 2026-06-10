def build_prompt(jewelry_type: str, jewelry_name: str, user_image_type: str = "face") -> str:
    # Diffusion models prefer descriptions of the final image rather than long rule lists
    if user_image_type == "hand":
        target_subject = "A photorealistic close-up of a hand and wrist"
        placement = f"wearing the {jewelry_name} naturally."
        preservation = "The skin texture, background, and lighting are exactly the same as the original hand image. No face or body is visible."
    else:
        target_subject = "A photorealistic portrait of a person"
        placement = f"wearing the {jewelry_name} naturally."
        preservation = "The person's facial identity, clothing, pose, and background are exactly the same as the original image."

    prompt = f"{target_subject} {placement} {preservation} The jewelry is perfectly blended with natural shadows and lighting, high-end commercial jewelry photography."
    return prompt.strip()


def build_prompt_with_context(
    jewelry_type: str,
    jewelry_name: str,
    user_image_type: str
) -> str:
    """
    Build a context-aware prompt.
    """
    return build_prompt(jewelry_type, jewelry_name, user_image_type)