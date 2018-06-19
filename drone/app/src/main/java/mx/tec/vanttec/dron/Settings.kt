package mx.tec.vanttec.dron

data class Setting(val key: String, val type: Setting.Type) {
    enum class Type {
        INT, FLOAT, BOOL, STRING
    }

    class UndefinedSettingTypeException(type: Type) : Exception("Undefined setting type: $type")
}