# Scope and Priority

1. Global configuration
   - include / exclude
   - alias
   - key serde
   - value serde
2. Per class configuration
   - include / exclude
   - alias
   - value serializer
3. Per field configuration
   - alias
   - converter
   - serializer / deserializer

What influences the scope and priority of configuration?

1. global configuration
   - any dict like object will be treated as global configuration
2. Per-class
   - Only decorated classes will be treated as per class configuration
3. Only decorated fields will be treated as per field configuration
