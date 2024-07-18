import rsa
public_key, private_key = rsa.newkeys(2048)


with open("public.pem", "wb") as w:
    w.write(public_key.save_pkcs1('PEM'))
with open("private.pem", "wb") as w:
    w.write(private_key.save_pkcs1('PEM'))

