from django.db import models

# Create your models here.
class RSAHistory(models.Model):
    public_key_n=models.BigIntegerField()
    public_key_e=models.BigIntegerField()
    private_key_d=models.BigIntegerField()
    
    original_number=models.BigIntegerField()
    encrypted_number=models.BigIntegerField(blank=True, null=True)
    
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"RSA History {self.id} - Original: {self.original_number}, Encrypted: {self.encrypted_number}"