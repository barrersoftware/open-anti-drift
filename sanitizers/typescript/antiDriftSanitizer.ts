/**
 * Universal Real-Time Token Sanitizer for TypeScript / JavaScript LLM Applications.
 * Prevents pronoun drift and corrects accidental misgendering in streaming web responses.
 */
export class AntiDriftSanitizer {
    private userName: string;
    private userGender: string;

    constructor(userName: string, userGender: string) {
        this.userName = userName;
        this.userGender = userGender.toLowerCase().trim();
    }

    public sanitizeText(text: string): string {
        if (!text) return text;

        const isFemale = this.userGender.includes("female") || this.userGender.includes("woman") || this.userGender.includes("she");
        const isMale = this.userGender.includes("male") || this.userGender.includes("man") || this.userGender.includes("he");

        if (!isFemale && !isMale) return text;

        let result = text;

        if (isFemale) {
            const replacements: [RegExp, string][] = [
                [new RegExp(`\\b${this.userName}\\s+(was|is|looks)\\s+he\\b`, "gi"), `${this.userName} $1 she`],
                [new RegExp(`\\b${this.userName}'s\\s+his\\b`, "gi"), `${this.userName}'s her`],
                [new RegExp(`\\bhe\\s+(said|looked|smiled)\\s+at\\s+${this.userName}\\b`, "gi"), `she $1 at ${this.userName}`],
            ];

            for (const [regex, replacement] of replacements) {
                result = result.replace(regex, replacement);
            }
        }

        return result;
    }

    public static extractThoughtBlock(text: string): { thought: string | null; visibleText: string } {
        const thoughtMatch = text.match(/<thought>([\s\S]*?)<\/thought>/);
        const thought = thoughtMatch ? thoughtMatch[1].trim() : null;
        const visibleText = text.replace(/<thought>[\s\S]*?<\/thought>/g, "").trim();

        return { thought, visibleText };
    }
}
