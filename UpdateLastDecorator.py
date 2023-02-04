from PyQt6.QtGui import QPixmap

from DrawableObject import DrawableObject


def get_collide(self, e):
    return self.camera.getCollide(e.position().x(), e.position().y(), self.objects)


def get_drawable(self, e):
    return DrawableObject(
        self.camera.abs(e.position().x()),
        0,
        self.camera.abs(e.position().y()),
        0,
        QPixmap(self.camera.abs_max_width(), self.camera.abs_max_height()))


def get_none(_, __):
    return None


def update_last(new_last_func):
    def update_last_decorator(func):
        def wrapper(self, e):
            if self.last_x is None:
                self.last_x = e.position().x()
                self.last_y = e.position().y()

                self.last_draw = new_last_func(self, e)
                return

            func(self, e)

            self.last_x = e.position().x()
            self.last_y = e.position().y()

        return wrapper

    return update_last_decorator


def update_last_cumulative(new_last_func):
    def update_last_decorator(func):
        def wrapper(self, e):
            if self.last_x is None:
                self.last_x = e.position().x()
                self.last_y = e.position().y()
                self.dx_cumulative = 0
                self.dy_cumulative = 0

                self.last_draw = new_last_func(self, e)
                return

            func(self, e)

            self.dx_cumulative = self.dx_cumulative + e.position().x() - self.last_x
            self.dy_cumulative = self.dy_cumulative + e.position().y() - self.last_y
            self.last_x = e.position().x()
            self.last_y = e.position().y()

        return wrapper

    return update_last_decorator
