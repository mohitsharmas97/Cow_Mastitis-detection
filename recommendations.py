"""
Treatment recommendations based on mastitis severity
"""

RECOMMENDATIONS = {
    'Mastitis-No': {
        'title': 'Healthy - No Mastitis Detected',
        'icon': '✅',
        'recommendations': [
            'Continue regular udder health monitoring',
            'Maintain proper milking hygiene practices',
            'Ensure clean and dry bedding',
            'Monitor for any changes in milk quality or udder appearance',
            'Follow routine vaccination schedule',
            'Schedule regular veterinary check-ups'
        ],
        'precautions': [
            'Keep milking equipment sanitized',
            'Practice proper pre and post-milking teat dipping',
            'Monitor feed quality and nutrition'
        ]
    },
    
    'Mastitis-Low': {
        'title': 'Mild Mastitis - Early Intervention Required',
        'icon': '⚠️',
        'recommendations': [
            'Monitor the cow closely for the next 24-48 hours',
            'Check for any changes in milk consistency or color',
            'Increase milking frequency if advised by veterinarian',
            'Apply warm compresses to the affected udder',
            'Ensure the cow is comfortable and stress-free',
            'Document any changes for veterinary consultation'
        ],
        'precautions': [
            'Isolate milk from affected quarters during treatment',
            'Consult veterinarian if condition worsens',
            'Ensure proper hydration',
            'Review and improve hygiene practices'
        ]
    },
    
    'Mastitis-Moderate': {
        'title': 'Moderate Mastitis - Veterinary Consultation Required',
        'icon': '⚠️',
        'recommendations': [
            '🔴 CONSULT A VETERINARIAN WITHIN 24 HOURS',
            'Begin antibiotic treatment as prescribed by veterinarian',
            'Increase milking frequency (every 4-6 hours)',
            'Apply hot and cold compresses alternately',
            'Monitor body temperature and general health',
            'Keep detailed records of symptoms and treatment',
            'Ensure adequate rest and nutrition'
        ],
        'precautions': [
            'DO NOT consume milk from affected quarters',
            'Follow antibiotic withdrawal periods strictly',
            'Maintain strict hygiene during treatment',
            'Monitor for signs of systemic infection (fever, depression)',
            'Consider reducing feed concentrate if prescribed'
        ]
    },
    
    'Mastitis-High': {
        'title': '🚨 Severe Mastitis - URGENT VETERINARY CARE NEEDED',
        'icon': '🚨',
        'recommendations': [
            '🔴 SEEK IMMEDIATE VETERINARY ATTENTION',
            '🔴 THIS IS A MEDICAL EMERGENCY',
            'Veterinarian may prescribe intensive antibiotic therapy',
            'Intravenous fluid therapy may be required',
            'Frequent stripping out of affected quarters (every 2-3 hours)',
            'Anti-inflammatory medication as prescribed',
            'Complete isolation from other animals',
            'Continuous monitoring of vital signs'
        ],
        'precautions': [
            'DO NOT DELAY - Contact veterinarian immediately',
            'Do not attempt home treatment without professional guidance',
            'Monitor for signs of shock or collapse',
            'Keep detailed medical records',
            'Follow all veterinary instructions precisely',
            'Prepare for possible hospitalization',
            'Consider prognosis discussion with veterinarian'
        ]
    }
}


def get_recommendations(severity):
    """
    Get treatment recommendations for a specific severity level
    
    Args:
        severity (str): Severity level (Mastitis-No, Low, Moderate, High)
    
    Returns:
        dict: Recommendations dictionary
    """
    return RECOMMENDATIONS.get(severity, RECOMMENDATIONS['Mastitis-Moderate'])


def format_recommendations_html(severity):
    """
    Format recommendations as HTML for display
    
    Args:
        severity (str): Severity level
    
    Returns:
        str: HTML formatted recommendations
    """
    rec = get_recommendations(severity)
    
    html = f"<h4>{rec['icon']} {rec['title']}</h4>"
    
    html += "<h5>Recommended Actions:</h5><ul>"
    for item in rec['recommendations']:
        html += f"<li>{item}</li>"
    html += "</ul>"
    
    html += "<h5>Precautions:</h5><ul>"
    for item in rec['precautions']:
        html += f"<li>{item}</li>"
    html += "</ul>"
    
    return html


def get_recommendations_text(severity):
    """
    Get recommendations as plain text for database storage
    
    Args:
        severity (str): Severity level
    
    Returns:
        str: Plain text recommendations
    """
    rec = get_recommendations(severity)
    
    text = f"{rec['title']}\n\n"
    text += "Recommendations:\n"
    for item in rec['recommendations']:
        text += f"- {item}\n"
    
    text += "\nPrecautions:\n"
    for item in rec['precautions']:
        text += f"- {item}\n"
    
    return text
