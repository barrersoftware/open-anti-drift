using System;
using System.Text.RegularExpressions;

namespace OpenAntiDrift.Sanitizer
{
    /// <summary>
    /// Universal Real-Time Token Sanitizer for C# / .NET Applications.
    /// </summary>
    public class AntiDriftSanitizer
    {
        public string UserName { get; }
        public string UserGender { get; }

        public AntiDriftSanitizer(string userName, string userGender)
        {
            UserName = userName;
            UserGender = userGender?.ToLowerInvariant().Trim() ?? "unspecified";
        }

        public string SanitizeText(string text)
        {
            if (string.IsNullOrWhiteSpace(text)) return text;

            bool isFemale = UserGender.Contains("female") || UserGender.Contains("woman") || UserGender.Contains("she");
            bool isMale = UserGender.Contains("male") || UserGender.Contains("man") || UserGender.Contains("he");

            if (!isFemale && !isMale) return text;

            var result = text;
            if (isFemale)
            {
                result = Regex.Replace(result, $@"\b{Regex.Escape(UserName)}\s+(was|is|looks)\s+he\b", $"{UserName} $1 she", RegexOptions.IgnoreCase);
                result = Regex.Replace(result, $@"\b{Regex.Escape(UserName)}'s\s+his\b", $"{UserName}'s her", RegexOptions.IgnoreCase);
            }
            return result;
        }

        public static (string? thought, string visibleText) ExtractThoughtBlock(string text)
        {
            if (string.IsNullOrWhiteSpace(text)) return (null, "");

            var match = Regex.Match(text, @"<thought>([\s\S]*?)</thought>");
            string? thought = match.Success ? match.Groups[1].Value.Trim() : null;
            string visibleText = Regex.Replace(text, @"<thought>[\s\S]*?</thought>", "").Trim();

            return (thought, visibleText);
        }
    }
}
