package open.antidrift.sanitizer

/**
 * Universal Real-Time Token Sanitizer for Kotlin / Android LLM Applications.
 */
class AntiDriftSanitizer(
    private val userName: String,
    private val userGender: String
) {
    fun sanitizeText(text: String): String {
        if (text.isBlank()) return text
        val uLower = userGender.lowercase().trim()
        val isFemale = uLower.contains("female") || uLower.contains("woman") || uLower.contains("she")
        val isMale = uLower.contains("male") || uLower.contains("man") || uLower.contains("he")

        if (!isFemale && !isMale) return text

        var result = text
        if (isFemale) {
            result = result.replace(Regex("\\b${Regex.escape(userName)}\\s+(was|is|looks)\\s+he\\b", RegexOption.IGNORE_CASE), "$userName $1 she")
            result = result.replace(Regex("\\b${Regex.escape(userName)}'s\\s+his\\b", RegexOption.IGNORE_CASE), "$userName's her")
        }
        return result
    }

    companion object {
        fun extractThoughtBlock(text: String): Pair<String?, String> {
            val match = Regex("<thought>([\\s\\S]*?)</thought>").find(text)
            val thought = match?.groupValues?.get(1)?.trim()
            val visibleText = text.replace(Regex("<thought>[\\s\\S]*?</thought>"), "").trim()
            return Pair(thought, visibleText)
        }
    }
}
