
// AttendVoice AI - Dashboard Navigation

const navLinks = document.querySelectorAll(".nav-link");
const sections = document.querySelectorAll(".content-section");

function showSection(sectionId) {
    sections.forEach(section => {
        section.classList.toggle("hidden", section.id !== sectionId);
    });

    navLinks.forEach(link => {
        link.classList.toggle(
            "active",
            link.dataset.section === sectionId
        );
    });

    const titles = {
        overview: "Dashboard Overview",
        students: "Student Management",
        voice: "Voice Attendance",
        subjects: "Subject Management",
        teachers: "Teacher Management",
        reports: "Attendance Reports"
    };

    document.querySelector(".topbar h1").textContent =
        titles[sectionId] || "Dashboard";
}

navLinks.forEach(link => {
    link.addEventListener("click", event => {
        event.preventDefault();
        showSection(link.dataset.section);
    });
});

// Quick action buttons

document.querySelectorAll("[data-go]").forEach(button => {
    button.addEventListener("click", () => {
        showSection(button.dataset.go);
    });
});

// Voice recognition

const startVoiceButton = document.getElementById("startVoice");
const voiceResult = document.getElementById("voiceResult");

if (startVoiceButton) {
    startVoiceButton.addEventListener("click", () => {

        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            voiceResult.textContent =
                "Voice recognition is not supported. Please use Google Chrome or Microsoft Edge.";
            return;
        }

        const recognition = new SpeechRecognition();

        recognition.lang = "en-IN";
        recognition.continuous = false;
        recognition.interimResults = false;

        voiceResult.textContent = "Listening... Speak a roll number.";

        startVoiceButton.disabled = true;

        recognition.onresult = event => {
            const spokenText =
                event.results[0][0].transcript;

            voiceResult.textContent =
                "You said: " + spokenText;
        };

        recognition.onerror = event => {
            voiceResult.textContent =
                "Voice error: " + event.error;
        };

        recognition.onend = () => {
            startVoiceButton.disabled = false;
        };

        try {
            recognition.start();
        } catch (error) {
            voiceResult.textContent =
                "Unable to start microphone. Please try again.";
            startVoiceButton.disabled = false;
        }
    });
}
