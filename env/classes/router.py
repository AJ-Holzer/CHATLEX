from typing import Any, Optional

import flet as ft  # type:ignore[import-untyped]

from env.config import config
from env.err.exceptions import ProgrammingError
from env.typing.dicts import PageContent, PageRoute


class AppRouter:
    def __init__(self, page: ft.Page) -> None:
        """Initialize a new PageRouter instance.

        Args:
            self(PageRouter): The PageRouter instance.
            page(ft.Page): The page object to associate with the router.

        Returns:
            None: No return value.

        Raises:
            TypeError: Raised if the provided page is not a valid ft.Page object.
        """
        # Page variables
        self._page: ft.Page = page

        # Define routes
        self._routes: PageRoute = {}

        # Define last routes
        self._last_routes: list[str] = []

    def add_route(self, route: str, content: PageContent) -> None:
        """Add a new route to the router.

        Args:
            self(Router): The router instance.
            route(str): The route path (e.g., '/home').
            content(PageContent): The content to associate with the route.

        Returns:
            None: No return value.

        Raises:
            ValueError: Raised if a route with the same name already exists.
        """
        if route in self._routes:
            raise ValueError(f"Route '{route}' already exists. Delete first!")

        # Add new route
        self._routes[route] = content

    def remove_route(self, route: str) -> None:
        if route in self._routes:
            del self._routes[route]

    def go(self, route: str) -> None:
        """Navigate to a specific route and execute associated actions.

        Args:
            self(RouteManager): Instance of the RouteManager class.
            route(str): The route to navigate to.

        Returns:
            None: No return value.

        Raises:
            ValueError: Raised if the specified route does not exist.
        """
        if not route.startswith("/"):
            raise ValueError(f"Route '{route}' does not start with a '/'!")

        if route not in self._routes:
            raise ValueError(f"Route '{route}' does not exist.")

        # Append current route to last routes if not the same route
        if len(self._last_routes) < 1 or self._last_routes[-1] != route:
            self._last_routes.append(route)

        self._page.clean()

        content: PageContent = self._routes[route]

        self._page.title = (
            f"{config.APP_TITLE}{config.APP_TITLE_SEPARATOR}{content['title']}"
        )
        self._page.add(*content["page_content"] if content["page_content"] else [])

        # Update the page
        self._page.update()  # type:ignore[union-attr]

        # Run the function if it exists
        if func := content["execute_function"]:
            args: Optional[list[Any] | dict[str, Any]] = content["function_args"]

            if isinstance(args, list):
                func(*args)
            elif isinstance(args, dict):
                func(**args)
            else:
                func()

    def pop(self) -> None:
        if len(self._last_routes) < 2:
            raise ProgrammingError(
                f"No route to pop. Already at initial route '{self._last_routes[-1]}'"
            )
        self._last_routes.pop()
        self.go(route=self._last_routes[-1])
