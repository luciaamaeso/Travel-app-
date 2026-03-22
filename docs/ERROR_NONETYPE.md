# 🆘 Error: 'NoneType' object has no attribute 'val'

## ¿Qué significa?

Este error significa que **Firebase no se inicializó correctamente** y la variable `ref` es `None`.

---

## ✅ Solución Rápida

### 1. Verifica el archivo de credenciales

**Debe estar en la RAÍZ del proyecto:**
```
Travel-app-/
├── serviceAccountKey.json  ← AQUÍ ✓
├── src/
├── docs/
└── ...
```

**NO aquí:**
```
Travel-app-/
├── src/
│   └── serviceAccountKey.json  ← ❌ INCORRECTO
```

### 2. Si está en el lugar equivocado, muévelo:
```bash
mv src/serviceAccountKey.json ./serviceAccountKey.json
```

### 3. Recarga la app:
```bash
# Si está ejecutándose, presiona Ctrl+C
# Luego ejecuta:
streamlit run src/app.py
```

---

## 🔍 Diagnosticar

Si el archivo está en el lugar correcto pero el error persiste:

```bash
bash firebase-diagnose.sh
```

Este script verificará todo automáticamente.

---

## 📋 Checklist

- [ ] ¿`serviceAccountKey.json` está en la raíz?
- [ ] ¿No está en `src/` o `docs/`?
- [ ] ¿El archivo es JSON válido?
  ```bash
  python3 -c "import json; json.load(open('serviceAccountKey.json')); print('✓ Válido')"
  ```
- [ ] ¿Recargaste la app (F5)?
- [ ] ¿Tienes internet?

---

## 📚 Más Información

- [FIREBASE_TROUBLESHOOTING.md](./FIREBASE_TROUBLESHOOTING.md)
- [SETUP_CREDENCIALES.md](./SETUP_CREDENCIALES.md)
- [FAQ.md](./FAQ.md)
