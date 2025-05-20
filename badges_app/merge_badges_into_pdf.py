from PyPDF2 import PdfWriter, PdfReader
from PyPDF2.generic._rectangle import RectangleObject
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black


class BadgeMerger:
    def __init__(self, badge_width_cm=7.5, badge_height_cm=12):
        self.badge_width = badge_width_cm * 28.35  # Convert cm to points
        self.badge_height = badge_height_cm * 28.35
        self.a4_center = (A4[0] / 2, A4[1] / 2)
        self.positions = {
            1: {
                1: (1, 0, 0, 1, self.a4_center[0] - self.badge_width, self.a4_center[1]),
                2: (1, 0, 0, 1, self.a4_center[0], self.a4_center[1]),
                3: (1, 0, 0, 1, self.a4_center[0] - self.badge_width, self.a4_center[1] - self.badge_height),
                4: (1, 0, 0, 1, self.a4_center[0], self.a4_center[1] - self.badge_height)
            },
            2: {
                1: (1, 0, 0, 1, self.a4_center[0], self.a4_center[1]),
                2: (1, 0, 0, 1, self.a4_center[0] - self.badge_width, self.a4_center[1]),
                3: (1, 0, 0, 1, self.a4_center[0], self.a4_center[1] - self.badge_height),
                4: (1, 0, 0, 1, self.a4_center[0] - self.badge_width, self.a4_center[1] - self.badge_height),
            }
        }

    def _draw_guide_lines(self):
        """Create a PDF page with cutting guide lines"""
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        can.setStrokeColor(black)
        can.setLineWidth(0.001)
        can.lines([
            (self.a4_center[0] - self.badge_width, self.a4_center[1] + self.badge_height,
             self.a4_center[0] - self.badge_width, self.a4_center[1] - self.badge_height),
            (self.a4_center[0] - self.badge_width, self.a4_center[1] + self.badge_height,
             self.a4_center[0] + self.badge_width, self.a4_center[1] + self.badge_height),
            (self.a4_center[0] - self.badge_width, self.a4_center[1] - self.badge_height,
             self.a4_center[0] + self.badge_width, self.a4_center[1] - self.badge_height),
            (self.a4_center[0] + self.badge_width, self.a4_center[1] + self.badge_height,
             self.a4_center[0] + self.badge_width, self.a4_center[1] - self.badge_height),
            (self.a4_center[0], self.a4_center[1] - self.badge_height,
             self.a4_center[0], self.a4_center[1] + self.badge_height)
        ])
        can.save()
        packet.seek(0)
        return PdfReader(packet).pages[0]

    def _create_page_template(self):
        """Create a blank PDF page template"""
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        can.drawString(0, 0, "")
        can.showPage()
        can.drawString(0, 0, "")
        can.save()
        packet.seek(0)
        return PdfReader(packet).pages[0], PdfReader(packet).pages[1]

    def _arrange_badges_on_page(self, badges_folder, badges, page_number):
        """Arrange 4 badges on a single page"""
        page_template, _ = self._create_page_template()

        for i, badge in enumerate(badges, 1):
            badge_path = os.path.join(badges_folder, badge)
            badge_reader = PdfReader(badge_path)
            badge_page = badge_reader.pages[0]

            badge_page.scale_to(self.badge_width, self.badge_height)
            badge_page.trimbox = RectangleObject([0.0, 0.0, A4[0], A4[1]])
            badge_page.add_transformation(self.positions[page_number][i])
            page_template.merge_page(badge_page)

        guide_lines = self._draw_guide_lines()
        page_template.merge_page(guide_lines)

        return page_template

    def merge_badges(self, badges_folder, output_file):
        """Merge all badges from folder into a single PDF with 4 badges per page"""
        pdf_writer = PdfWriter()
        all_badges = sorted([f for f in os.listdir(badges_folder) if f.endswith('.pdf')])

        for i in range(0, len(all_badges), 4):
            badges_batch = all_badges[i:i + 4]

            # Create two pages (front and back) for each 4 badges
            front_page = self._arrange_badges_on_page(badges_folder, badges_batch, 1)
            back_page = self._arrange_badges_on_page(badges_folder, badges_batch, 2)

            pdf_writer.add_page(front_page)
            pdf_writer.add_page(back_page)

        with open(output_file, "wb") as f:
            pdf_writer.write(f)


if __name__ == "__main__":
    merger = BadgeMerger(badge_width_cm=7.5, badge_height_cm=12)
    merger.merge_badges("stamped", "final_badges.pdf")
