"""
API client for FastAPI prediction backend.

This module provides functions to:
- Call the /predict endpoint
- Handle timeouts and errors
- Format responses for Streamlit display
"""

import os
from typing import Any
import requests
from requests.exceptions import RequestException, Timeout


# API configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
PREDICT_ENDPOINT = f"{API_URL}/predict"
REQUEST_TIMEOUT = 10  # 10 seconds


def call_predict_api(inputs: dict[str, Any]) -> dict[str, Any]:
    """
    Call the FastAPI prediction endpoint.

    Args:
        inputs: Dictionary with 15 prediction input fields

    Returns:
        Dictionary with either:
        - Success: {"probability": float, "prediction": str, "threshold": float}
        - Error: {"error": str, "message": str, "details": list} (details optional)

    Error Types:
        - "timeout": Request took longer than 10 seconds
        - "validation": Server rejected inputs (422 error)
        - "server": Server error (500 error)
        - "network": Connection failed or other network error
    """
    try:
        response = requests.post(
            PREDICT_ENDPOINT,
            json=inputs,
            timeout=REQUEST_TIMEOUT,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        # Check for HTTP errors
        if response.status_code == 200:
            # Success - return prediction result
            return response.json()

        elif response.status_code == 422:
            # Validation error - parse field errors
            error_data = response.json()
            details = error_data.get("detail", [])

            # Format validation errors for display
            error_messages = []
            for err in details:
                field = err.get("loc", ["unknown"])[-1]  # Get field name
                msg = err.get("msg", "Invalid value")
                error_messages.append(f"{field}: {msg}")

            return {
                "error": "validation",
                "message": "Les données saisies sont invalides.",
                "details": details,
                "formatted_errors": error_messages
            }

        elif response.status_code >= 500:
            # Server error
            error_data = response.json() if response.text else {}
            detail = error_data.get("detail", "Erreur serveur inconnue")

            return {
                "error": "server",
                "message": f"Une erreur s'est produite côté serveur: {detail}",
                "status_code": response.status_code
            }

        else:
            # Other HTTP errors
            return {
                "error": "http",
                "message": f"Erreur HTTP {response.status_code}",
                "status_code": response.status_code
            }

    except Timeout:
        # Request timeout
        return {
            "error": "timeout",
            "message": "Le service met trop de temps à répondre (>10s). Veuillez réessayer dans quelques instants."
        }

    except ConnectionError:
        # Connection failed
        return {
            "error": "connection",
            "message": "Impossible de se connecter au service de prédiction. Vérifiez que l'API est démarrée."
        }

    except RequestException as e:
        # Generic network/request error
        return {
            "error": "network",
            "message": f"Service temporairement indisponible: {str(e)}"
        }

    except Exception as e:
        # Unexpected error
        return {
            "error": "unknown",
            "message": f"Erreur inattendue: {str(e)}"
        }


def is_success_response(response: dict[str, Any]) -> bool:
    """
    Check if API response is a success.

    Args:
        response: Response dictionary from call_predict_api()

    Returns:
        True if response contains prediction result, False if error
    """
    return "error" not in response and "probability" in response


def format_error_message(response: dict[str, Any]) -> str:
    """
    Format error response into user-friendly message.

    Args:
        response: Error response from call_predict_api()

    Returns:
        Formatted error message for display
    """
    if is_success_response(response):
        return ""

    error_type = response.get("error", "unknown")
    base_message = response.get("message", "Une erreur s'est produite")

    if error_type == "validation" and "formatted_errors" in response:
        errors = "\n- ".join(response["formatted_errors"])
        return f"{base_message}\n\nErreurs détectées:\n- {errors}"

    return base_message


def get_api_endpoint() -> str:
    """
    Get the configured API endpoint URL.

    Returns:
        Full URL to the predict endpoint
    """
    return PREDICT_ENDPOINT


def set_api_url(url: str) -> None:
    """
    Override the API URL (useful for testing).

    Args:
        url: Base API URL (e.g., "http://localhost:8000")
    """
    global API_URL, PREDICT_ENDPOINT
    API_URL = url
    PREDICT_ENDPOINT = f"{API_URL}/predict"
