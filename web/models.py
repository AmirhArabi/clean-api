import base64
from django.db import models
import qrcode
from io import BytesIO
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask


# create a model to save the url
class Url(models.Model):
    url = models.CharField(max_length=200)
    short_url = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    click_count = models.IntegerField(default=0)
    qr_code = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.url + " => " + self.short_url + " => " + str(self.click_count)

    def save(self, *args, **kwargs):
        data = "http://api.amirharabi.tech/" + self.short_url
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(data)
        img = qr.make_image(image_factory=StyledPilImage,
                            module_drawer=RoundedModuleDrawer(),
                            color_mask=RadialGradiantColorMask(
                                back_color=(255, 255, 255),
                                center_color=(6, 10, 59),
                                edge_color=(25, 5, 30)
                            ),
                            fit=True,
                            )

        buffer = BytesIO()
        img.save(buffer)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        self.qr_code = image_base64
        super().save(*args, **kwargs)
