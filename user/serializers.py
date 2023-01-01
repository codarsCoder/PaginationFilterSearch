# bu app user işlemlerini yönetmek için yazıldı app için model yazmadık çünkü django nun hazır user yapısı zaten var
from rest_framework import serializers
from django.contrib.auth.models import User # user işlemleri için bunu import ettik bu djangonun user modeli bununla user db ye ulaşacağız, user için hazır modeli kullanacağız extra model oluşturma zaahmetindn kurtuldu
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True, validators=[UniqueValidator(queryset=User.objects.all())]) # bu alan modelde required eğil ama biz vaildsayonda required olarak override ettik
    ## birde bu email uniq olsun istiyoruz db de tekrar etmesin onuda buradan kontrol etmek için drf uniqvalidator kullanacağız  https://www.django-rest-framework.org/api-guide/validators/#uniquevalidator
    password = serializers.CharField(write_only = True) # sadece post(yazma işlemlerinde validasyon sağlyacak bir get işleminde devrede olmayacak ) read_only deseydik create işlemlerinde kullanılmayacaktı
    password2 = serializers.CharField(write_only = True, required = True) #modelde bu kısım yok burada password kontrol için validasyona katıyoruz
    
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password2'
        )
    
    ## aşağıdaki işlemleri ModelSerializer oto yapıyor ama biz manuel yaptıracağız çünkü password2  karşılaştırması yapacağız
    def validate(self, data): #burası validasyon yapmak için yazılır içinde şartlı işlemleri kontrol ederiz
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Password fields didnt match.'})   
        return data 
    ## aslında burada create metodunu override ediyoruz
    def create(self, validated_data):  ## biz validasyon işlemi için passwordleri işe kattık ama onlar dbye kaydedilmeyecek bu yüzden manuel kayıt işlemi gerçekleştirmek gerekiyor  bu kısımda   ve validasyon sonrsı db ye kayıt sağlar
       
        # password2 kullanılmayacağı için dictten çıkardık
        validated_data.pop('password2')
        # password u daha sonra set etmek için değişkene atadık.
        password = validated_data.pop('password')
        # username=validate_data['username], email = va.......
        user = User.objects.create(**validated_data)  #user modeline validated datayı kaydet
        # password ün encrypte olarak db ye kaydedilmesiniş sağlıyor.
        user.set_password(password) #yeni user pass kaydetmeliyiz
        user.save()
        return user
    
    ### NOT aslında bu metod çağırıldığında kendi içnde bulunan create de extend edilip kullanılabiliyor   aşağıdaki gibi bir kullanımda işimizi görür yukarıdaki daha kolay 
    # def create(self, validated_data):
    #     response =  super().create(validated_data) # burada ki create içinde data respons ediliyor
    #     token = Token.objects.create(user_id=response.data['id']) # user modelindeki id yi burası user_id olarak tanıyor 
    #     response.data['token'] = token.key
    #     return response