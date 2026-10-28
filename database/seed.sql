-- TaskMate Seed Data
-- Initial FAQs and Sample Tasks

USE taskmate_db;

-- Clear and insert default FAQs (at least 12 required)
INSERT INTO faqs (question, answer, category) VALUES
(
    'What is TaskMate?',
    'TaskMate is an AI-powered personal task management web application designed to help students and professionals organize everyday to-dos, track priorities, and get instant assistance via an integrated chatbot.',
    'General'
),
(
    'How do I create a task?',
    'To create a task, navigate to the Home page dashboard, locate the "Add New Task" form, enter a task title (required), optional description, select a priority (Low, Medium, High), choose an optional due date, and click the "Add Task" button.',
    'Tasks'
),
(
    'How do I edit a task?',
    'Find the task card in your dashboard list, click the "Edit" button, modify the title, description, priority, or due date in the edit modal, and click "Save Changes".',
    'Tasks'
),
(
    'How do I delete a task?',
    'Click the "Delete" button on any task card and confirm the deletion. The task will be permanently removed from the database.',
    'Tasks'
),
(
    'How do I mark a task as completed?',
    'Click the checkmark or "Complete" button on any pending task card. The task status will update immediately to completed and update your dashboard completion stats.',
    'Tasks'
),
(
    'Can I reopen a completed task?',
    'Yes! On any completed task card, click the "Reopen" button. The task will return to pending status and recalculate your progress statistics.',
    'Tasks'
),
(
    'How do I filter my tasks?',
    'Use the filter tabs located above the task list: "All Tasks" displays everything, "Pending" displays only active tasks, and "Completed" shows finished items.',
    'Tasks'
),
(
    'What do the task priority levels mean?',
    'TaskMate provides three priority levels: High (urgent and important, highlighted in red), Medium (standard everyday items, highlighted in amber), and Low (minor or flexible tasks, highlighted in green).',
    'Tasks'
),
(
    'Where are my tasks stored?',
    'Your tasks, FAQs, and support tickets are stored reliably in a relational MySQL database (with local development fallback support). Chat conversations and feedback are stored in MongoDB.',
    'Technical'
),
(
    'What should I do if the website is unavailable?',
    'First, check your internet connection. If the issue persists, check the server health endpoint at /health or refer to the Error Guide page for HTTP 500/503 troubleshooting. You can also submit a support ticket.',
    'Troubleshooting'
),
(
    'How can I contact support?',
    'You can open the AI Assistant widget at the bottom-right of any page and request a support ticket, or submit a ticket when the assistant is unable to resolve your inquiry. You will receive a unique ticket ID (e.g., TKT-2026-0001).',
    'Support'
),
(
    'How does the AI assistant work?',
    'The TaskMate AI Assistant is an agent grounded on our MySQL FAQ knowledge base, error code directory, and live tasks. It utilizes Groq API (Llama 3.3) for high-speed reasoning and tool execution, with automatic offline fallback when external AI is unreachable.',
    'AI Assistant'
);

-- Sample starter tasks
INSERT INTO tasks (title, description, priority, due_date, is_completed) VALUES
('Welcome to TaskMate!', 'Explore the dashboard, try editing or completing this task, and ask the AI assistant any questions.', 'High', DATE_ADD(CURRENT_DATE, INTERVAL 1 DAY), FALSE),
('Review Final Project Checklist', 'Ensure all 17 phases are completed, tested, and ready for evaluation.', 'High', DATE_ADD(CURRENT_DATE, INTERVAL 3 DAY), FALSE),
('Explore Error Code Guide', 'Check /errors to learn about HTTP 400, 401, 403, 404, 429, 500, 503, and DEV001.', 'Medium', DATE_ADD(CURRENT_DATE, INTERVAL 5 DAY), TRUE);
