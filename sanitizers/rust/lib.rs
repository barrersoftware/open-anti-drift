use regex::Regex;

pub struct AntiDriftSanitizer {
    pub user_name: String,
    pub user_gender: String,
}

impl AntiDriftSanitizer {
    pub fn new(user_name: &str, user_gender: &str) -> Self {
        AntiDriftSanitizer {
            user_name: user_name.to_string(),
            user_gender: user_gender.to_lowercase().trim().to_string(),
        }
    }

    pub fn sanitize_text(&self, text: &str) -> String {
        if text.is_empty() {
            return text.to_string();
        }

        let is_female = self.user_gender.contains("female") || self.user_gender.contains("woman") || self.user_gender.contains("she");
        if !is_female {
            return text.to_string();
        }

        let pattern = format!(r"\b{}\s+(was|is|looks)\s+he\b", regex::escape(&self.user_name));
        if let Ok(re) = Regex::new(&pattern) {
            return re.replace_all(text, format!("{} $1 she", self.user_name)).to_string();
        }

        text.to_string()
    }

    pub fn extract_thought_block(text: &str) -> (Option<String>, String) {
        let re_thought = Regex::new(r"(?s)<thought>(.*?)</thought>").unwrap();
        let thought = re_thought.captures(text).map(|caps| caps[1].trim().to_string());
        let visible_text = re_thought.replace_all(text, "").trim().to_string();

        (thought, visible_text)
    }
}
