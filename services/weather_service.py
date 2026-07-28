from __future__ import annotations


class WeatherService:
    """
    Placeholder Weather Service.

    This service can later be connected to OpenWeatherMap,
    WeatherAPI, or any other provider.
    """

    def get_weather(
        self,
        location: str | None = None,
    ) -> str:

        if location:
            return (
                f"Weather service is not configured yet "
                f"for '{location}'."
            )

        return "Weather service is not configured yet."


weather_service = WeatherService()