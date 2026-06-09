def build_prompt(jewelry_type: str, jewelry_name: str) -> str:
    """
    Build a detailed prompt for Gemini based on jewelry type.
    
    Args:
        jewelry_type: Type of jewelry (necklace, earrings, ring, bracelet)
        jewelry_name: Name of the jewelry item
    
    Returns:
        Detailed prompt for Gemini image generation
    """
    
    base_prompt = f"""You are an expert jewelry visualization specialist. Your task is to create a photorealistic virtual try-on image of {jewelry_name} on the provided image.

CRITICAL REQUIREMENTS:

IDENTITY PRESERVATION:
- Preserve the face exactly as shown in the original image
- Maintain skin tone accurately
- Keep hairstyle unchanged
- Preserve facial expression
- Keep all facial features in their original positions

JEWELRY PLACEMENT AND PRESENTATION:
- The {jewelry_name} must be placed appropriately
- Maintain the jewelry's original shape and appearance
- Preserve all colors and materials exactly as shown
- Keep gemstone details and texture visible
- Match the jewelry scale to the image proportions

REALISM AND LIGHTING:
- Match the lighting conditions from the original image
- Apply appropriate shadows and highlights
- Ensure the jewelry sits naturally on the body
- Create seamless integration with the skin
- Maintain photorealistic quality throughout

BACKGROUND PRESERVATION:
- Keep the original background exactly as it appears
- Do not modify any background elements
- Maintain the same lighting environment

"""
    
    jewelry_specific_prompts = {
        "necklace": """
NECKLACE-SPECIFIC INSTRUCTIONS:
- Place the necklace around the neck only
- Ensure it hangs naturally from the shoulders
- Position it at an appropriate depth on the chest
- Maintain proper draping and alignment
- Preserve the neckline and shoulders
- Show how the necklace complements the face and neck
""",
        "earrings": """
EARRINGS-SPECIFIC INSTRUCTIONS:
- Place earrings on both ears if a front-facing image, or the visible ear
- Position them at the correct earlobe level
- Ensure they dangle naturally if they are dangly style
- Show proper alignment with the ear structure
- Maintain the hairstyle around the ears
- Display how earrings frame the face
""",
        "ring": """
RING-SPECIFIC INSTRUCTIONS:
- Place the ring on the appropriate finger in the hand image
- Show the ring from a flattering angle
- Ensure proper fit and positioning on the finger
- Display gemstones and details clearly
- Maintain natural hand positioning
- Show realistic shadow and shine on the ring
- Preserve the hand's natural skin tone
""",
        "bracelet": """
BRACELET-SPECIFIC INSTRUCTIONS:
- Place the bracelet around the wrist
- Position it naturally as it would sit on the arm
- Show the bracelet from a clear viewing angle
- Ensure proper placement that doesn't look forced
- Maintain natural arm positioning
- Display the bracelet's details and shine
- Preserve the wrist and arm's natural appearance
"""
    }
    
    prompt = base_prompt + jewelry_specific_prompts.get(jewelry_type, "")
    
    prompt += """
OUTPUT REQUIREMENTS:
- Generate a single, high-quality photorealistic image
- The image should look like a professional jewelry try-on photo
- Dimensions should match the input image proportions
- The result should be ready for product showcase
- Ensure all details are crisp and clear

FINAL INSTRUCTION:
Create the virtual try-on image now. Remember: preserve identity, maintain realism, and perfect jewelry placement.
"""
    
    return prompt


def build_prompt_with_context(jewelry_type: str, jewelry_name: str, user_image_type: str) -> str:
    """
    Build a context-aware prompt based on jewelry type and image context.
    
    Args:
        jewelry_type: Type of jewelry
        jewelry_name: Name of jewelry
        user_image_type: Type of user image (face or hand)
    
    Returns:
        Detailed contextualized prompt
    """
    prompt = build_prompt(jewelry_type, jewelry_name)
    
    context_additions = {
        "face": "\nIMPORTANT: The provided image shows a face/person. Apply the jewelry appropriately to the face region.",
        "hand": "\nIMPORTANT: The provided image shows a hand. Apply the jewelry appropriately to the hand/wrist region."
    }
    
    prompt += context_additions.get(user_image_type, "")
    
    return prompt
