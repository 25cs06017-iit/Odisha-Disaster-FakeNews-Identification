def generate_advisory(retrieved_fact_text):
    """Simulate LLM-based advisory generation using a safe template.
    Uses the verified fact text (from Cyclone Fani dataset) as the
    core evidence.
    """
    template = f"""Official Advisory – Cyclone-Related Public Information

Authorities confirm the following verified information:
{retrieved_fact_text}

Residents are requested to rely only on official announcements from the Indian
Meteorological Department (IMD), Odisha State Disaster Management Authority (OSDMA),
and local administration. Relief, power restoration and essential services are
being monitored by authorities.

If you require assistance, call official helplines such as 1070 or your local
emergency number. Please avoid sharing unverified information, images, or videos.
Stay indoors if advised, stay calm, and follow government updates.
"""
    return template
