from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model

User = get_user_model()

GENDER = [
    ('M','Homme'),
    ('F','Femme'),
    ('U','Unisex'),
]
WILAYAS = [
    ('01', 'Adrar'),
    ('02', 'Chlef'),
    ('03', 'Laghouat'),
    ('04', 'Oum El Bouaghi'),
    ('05', 'Batna'),
    ('06', 'Béjaïa'),
    ('07', 'Biskra'),
    ('08', 'Béchar'),
    ('09', 'Blida'),
    ('10', 'Bouira'),
    ('11', 'Tamanghasset'),
    ('12', 'Tébessa'),
    ('13', 'Tlemcen'),
    ('14', 'Tiaret'),
    ('15', 'Tizi Ouzou'),
    ('16', 'Alger'),
    ('17', 'Djelfa'),
    ('18', 'Jijel'),
    ('19', 'Sétif'),
    ('20', 'Saïda'),
    ('21', 'Skikda'),
    ('22', 'Sidi Bel Abbès'),
    ('23', 'Annaba'),
    ('24', 'Guelma'),
    ('25', 'Constantine'),
    ('26', 'Médéa'),
    ('27', 'Mostaganem'),
    ('28', 'M\'Sila'),
    ('29', 'Mascara'),
    ('30', 'Ouargla'),
    ('31', 'Oran'),
    ('32', 'El Bayadh'),
    ('33', 'Illizi'),
    ('34', 'Bordj Bou Arreridj'),
    ('35', 'Boumerdès'),
    ('36', 'El Taref'),
    ('37', 'Tindouf'),
    ('38', 'Tissemsilt'),
    ('39', 'El Oued'),
    ('40', 'Khenchela'),
    ('41', 'Souk Ahras'),
    ('42', 'Tipaza'),
    ('43', 'Mila'),
    ('44', 'Aïn Defla'),
    ('45', 'Naâma'),
    ('46', 'Aïn Témouchent'),
    ('47', 'Ghardaïa'),
    ('48', 'Relizane'),
    ('49', 'Timimoun'),
    ('50', 'Bordj Badji Mokhtar'),
    ('51', 'Ouled Djellal'),
    ('52', 'Béni Abbès'),
    ('53', 'In Salah'),
    ('54', 'In Guezzam'),
    ('55', 'Touggourt'),
    ('56', 'Djanet'),
    ('57', 'El M\'Ghair'),
    ('58', 'El Menia'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    wilaya = models.CharField(max_length=2, choices=WILAYAS, null=True, blank=True) 
    picture = models.ImageField(upload_to='profilepics/', default='profilepics/default_pp.png')
    phone_number = PhoneNumberField(unique =True, null=True, blank=True)

    # birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(choices=GENDER, max_length=1, default='U')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    taille = models.CharField(max_length=4, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class PostPicture(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pictures')
    image = models.ImageField(upload_to='post_images/')

class Chat(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='chats')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class Article_Panier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.post.title

class Article_Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.post.title

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.post.title)+" "+str(self.user.username)