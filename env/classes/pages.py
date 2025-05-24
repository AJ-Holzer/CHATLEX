from typing import Optional

import flet as ft  # type:ignore[import-untyped]

from env.types.typing import (
    PageContent,
    SitePages,
)


class Router:
    def __init__(
        self,
        page: ft.Page,
        start_route: str,
    ) -> None:
        self._page: ft.Page = page
        self._default_title: str = self._page.title
        self._start_route: str = start_route
        self._routes: SitePages = {}
        self._current_route: Optional[str] = None

    def _retrieve_content(self, route: str) -> list[ft.Control]:
        """Retrieves the content associated with a given route.

        Args:
            self(Any): Instance of the class.
            route(str): The route to retrieve content from.

        Returns:
            list[ft.Control]: A list of ft.Control objects representing the content. Returns a default message if no content is found for the given route.

        Raises:
            ValueError: Raised when the specified route does not exist.
        """
        if route not in self._routes:
            raise ValueError(f"The page '{route}' does not exist!")

        return self._routes[route].get(
            "content",
            [
                ft.Text(value=f"No content found for '{route}'!"),
            ],
        )

    def add(self, route: str, content: PageContent) -> None:
        """Adds a new route and its associated content to the internal routes dictionary.

        Args:
            self(RouteManager): Instance of the RouteManager class.
            route(str): The route path to add (e.g., '/home').
            content(PageContent): The content associated with the route.

        Returns:
            None: This function does not return a value.

        Raises:
            KeyError: If the route already exists.
        """
        if route in self._routes:
            raise ValueError("Route already exists!")
        self._routes[route] = content

    def go(self, route: str) -> None:
        """Navigate to a specific route and render its associated controls.

        Args:
            self(Self): Instance of the class.
            route(str): The name of the route to navigate to.

        Returns:
            None: No return value.

        Raises:
            ValueError: Raised when no route exists for the provided 'route' name.
        """
        if route not in self._routes:
            raise ValueError(f"No route exists for route '{route}'!")

        self._page.clean()

        controls: list[ft.Control] = self._routes[route].get("content", [])

        # Check if controls exist and are not empty
        if not controls:
            raise ValueError(f"No route exists for route '{route}'!")

        # Go to route
        self._current_route = route
        self._page.add(*controls)

        # Update title
        if title := self._routes[route].get("title"):
            self._page.title = f"{self._default_title} - {title}"
            print(f"Changing title to '{f"{self._default_title} - {title}"}'")
        else:
            self._page.title = self._default_title

        self._page.update()  # type:ignore

    def route_pop(self) -> None:
        """Removes the last element from the current view path.

        Args:
            self(Route): The Route instance.

        Returns:
            None: No return value.

        Raises:
            RuntimeError: Raised when attempting to pop from an empty path (i.e., when '_current_route' is None).
        """
        if not self._current_route:
            raise RuntimeError("Cannot pop the current path because it is 'None'.")

        # Remove last element of the route
        route_parts: list[str] = self._current_route.split("/")
        self._current_route = "/".join(route_parts[: len(route_parts) - 1 :])

        # Go to new route
        self.go(route=self._current_route)
