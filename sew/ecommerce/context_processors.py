from .models import Master,Category

def website_info(request):
    """Fetch website details dynamically from Master model"""
    info = {
        "website_name": Master.objects.filter(name="Website Name").first(),

        "address": Master.objects.filter(name="Address").first(),
        "phone": Master.objects.filter(name="Phone").first(),
        "email": Master.objects.filter(name="Email").first(),
        "social_links": {
            "twitter": Master.objects.filter(name="Twitter").first(),
            "facebook": Master.objects.filter(name="Facebook").first(),
            "instagram": Master.objects.filter(name="Instagram").first(),
            "linkedin": Master.objects.filter(name="LinkedIn").first(),
        },

    }
    category=Category.objects.all()
    result = {"categories":category}
    for key, value in info.items():
        if isinstance(value, dict):
            # Handling social links which is a nested dictionary
            result[key] = {social_key: social_value.description if social_value else "#" for social_key, social_value in value.items()}
        else:
            # For other keys, just store the description (or fallback to "#" if not found)
            result[key] = value.description if value else "#"
    
    print("this is resulr ...............",result)
    return result
    
