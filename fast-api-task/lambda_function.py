from mangum import Mangum
from customers import app

handler = Mangum(app)
