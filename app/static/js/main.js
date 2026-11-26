document.addEventListener("DOMContentLoaded", function () {
    // Auto-dismiss flash alerts after 4.5 seconds
    const alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach(function (alertEl) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 4500);
    });

    // Live grade preview on grades/form.html (40% CC + 60% Exam)
    const ccInput = document.getElementById("continuous_assessment");
    const examInput = document.getElementById("exam_score");
    const previewOutput = document.getElementById("final_grade_preview");

    if (ccInput && examInput && previewOutput) {
        const updateGradePreview = () => {
            const cc = Math.min(20, Math.max(0, parseFloat(ccInput.value) || 0));
            const exam = Math.min(20, Math.max(0, parseFloat(examInput.value) || 0));
            const finalGrade = (0.4 * cc + 0.6 * exam).toFixed(2);
            previewOutput.textContent = `${finalGrade} / 20`;
            previewOutput.className = parseFloat(finalGrade) >= 10
                ? "badge bg-success fs-6"
                : "badge bg-danger fs-6";
        };
        ccInput.addEventListener("input", updateGradePreview);
        examInput.addEventListener("input", updateGradePreview);
        updateGradePreview();
    }
});