"""
Email sending module for ZEE STUDY.
Configure via environment variables:
  MAIL_SERVER   — SMTP host (default: smtp.gmail.com)
  MAIL_PORT     — SMTP port (default: 587)
  MAIL_USERNAME — sender email address
  MAIL_PASSWORD — sender email password / app password
  MAIL_FROM     — display name + address, e.g. "ZEE STUDY <noreply@zeequiz.co.uk>"
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MAIL_SERVER   = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT     = int(os.environ.get('MAIL_PORT', 587))
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
MAIL_FROM     = os.environ.get('MAIL_FROM', f'ZEE STUDY <{MAIL_USERNAME}>')


def _send(to_email, subject, html_body, text_body=''):
    """Low-level send — raises on failure."""
    if not MAIL_USERNAME or not MAIL_PASSWORD:
        print(f'[mailer] Email not configured — would have sent to {to_email}: {subject}')
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From']    = MAIL_FROM
    msg['To']      = to_email

    if text_body:
        msg.attach(MIMEText(text_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_USERNAME, to_email, msg.as_string())

    return True


def send_welcome(to_email, username):
    subject = '👋 Welcome to ZEE STUDY!'
    html = f'''
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
      <div style="background:#2e7d32;padding:24px;text-align:center;border-radius:8px 8px 0 0">
        <h1 style="color:#fff;margin:0;font-size:28px">ZEE STUDY</h1>
        <p style="color:#a5d6a7;margin:4px 0 0">GCSE Science Quiz</p>
      </div>
      <div style="background:#fff;padding:32px;border:1px solid #e8f5e9;border-radius:0 0 8px 8px">
        <h2 style="color:#1b5e20">Welcome, {username}! 🎉</h2>
        <p style="color:#546e7a">Your account is ready. Start revising Biology, Chemistry and Physics with over 1,900 GCSE questions.</p>
        <div style="text-align:center;margin:32px 0">
          <a href="https://zeequiz.co.uk"
             style="background:#2e7d32;color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:bold;font-size:16px">
            Start Revising →
          </a>
        </div>
        <p style="color:#90a4ae;font-size:13px">Good luck with your GCSEs! The ZEE STUDY team 🔬</p>
      </div>
    </div>
    '''
    text = f'Welcome to ZEE STUDY, {username}! Visit https://zeequiz.co.uk to start revising.'
    try:
        _send(to_email, subject, html, text)
    except Exception as e:
        print(f'[mailer] Failed to send welcome to {to_email}: {e}')


def send_reminder(to_email, username, days_inactive):
    subject = f'📚 We miss you, {username}! Come back and revise'
    html = f'''
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
      <div style="background:#2e7d32;padding:24px;text-align:center;border-radius:8px 8px 0 0">
        <h1 style="color:#fff;margin:0;font-size:28px">ZEE STUDY</h1>
        <p style="color:#a5d6a7;margin:4px 0 0">GCSE Science Quiz</p>
      </div>
      <div style="background:#fff;padding:32px;border:1px solid #e8f5e9;border-radius:0 0 8px 8px">
        <h2 style="color:#1b5e20">Hey {username}, it&rsquo;s been {days_inactive} days! 👋</h2>
        <p style="color:#546e7a">Regular revision is the best way to improve your GCSE grades.
        Even 10 minutes a day makes a big difference.</p>
        <div style="background:#f1f8f1;border-left:4px solid #2e7d32;padding:16px;margin:20px 0;border-radius:0 8px 8px 0">
          <p style="margin:0;color:#1b5e20;font-weight:600">💡 Did you know?</p>
          <p style="margin:8px 0 0;color:#546e7a">Students who revise daily score on average 20% higher in their GCSEs.</p>
        </div>
        <div style="text-align:center;margin:32px 0">
          <a href="https://zeequiz.co.uk"
             style="background:#2e7d32;color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:bold;font-size:16px">
            Continue Revising →
          </a>
        </div>
        <p style="color:#90a4ae;font-size:13px">You&rsquo;re receiving this because you registered at ZEE STUDY.</p>
      </div>
    </div>
    '''
    text = f'Hey {username}, you haven\'t revised in {days_inactive} days. Visit https://zeequiz.co.uk to keep your streak going!'
    try:
        _send(to_email, subject, html, text)
    except Exception as e:
        print(f'[mailer] Failed to send reminder to {to_email}: {e}')


def send_quiz_report(to_email, username, subject_name, topic_name, score, total, percentage, wrong_answers):
    grade = '🌟 Excellent' if percentage == 100 else '✅ Great' if percentage >= 70 else '👍 Good effort' if percentage >= 50 else '💪 Keep practising'
    subject_line = f'Your {subject_name} quiz result — {percentage}%'
    html = f'''
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
      <div style="background:#2e7d32;padding:24px;text-align:center;border-radius:8px 8px 0 0">
        <h1 style="color:#fff;margin:0;font-size:28px">ZEE STUDY</h1>
        <p style="color:#a5d6a7;margin:4px 0 0">Quiz Report</p>
      </div>
      <div style="background:#fff;padding:32px;border:1px solid #e8f5e9;border-radius:0 0 8px 8px">
        <h2 style="color:#1b5e20">{grade}, {username}!</h2>
        <p style="color:#546e7a"><strong>{subject_name}</strong> — {topic_name}</p>
        <div style="text-align:center;background:#f1f8f1;border-radius:50%;width:100px;height:100px;
                    display:flex;align-items:center;justify-content:center;margin:20px auto;
                    border:4px solid {'#2e7d32' if percentage>=70 else '#f59e0b' if percentage>=50 else '#ef4444'}">
          <div>
            <div style="font-size:28px;font-weight:bold;color:#1b5e20">{percentage}%</div>
            <div style="font-size:13px;color:#546e7a">{score}/{total}</div>
          </div>
        </div>
        {'<div style="margin-top:24px"><h3 style="color:#b71c1c">Questions to Review</h3>' + ''.join([f'<div style="background:#fff5f5;border-left:3px solid #ef4444;padding:12px;margin:8px 0;border-radius:0 6px 6px 0"><p style="margin:0;font-weight:600;color:#1a1a1a">{w["question_text"]}</p><p style="margin:6px 0 0;color:#ef4444;font-size:13px">✗ Your answer: {w.get("user_answer","?")} — {w.get("user_answer_text","")}</p><p style="margin:4px 0 0;color:#2e7d32;font-size:13px">✓ Correct: {w["correct_answer"]} — {w.get("correct_answer_text","")}</p><p style="margin:4px 0 0;color:#546e7a;font-size:12px">{w.get("explanation","")}</p></div>' for w in wrong_answers[:5]]) + '</div>' if wrong_answers else ''}
        <div style="text-align:center;margin:32px 0">
          <a href="https://zeequiz.co.uk"
             style="background:#2e7d32;color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:bold">
            Take Another Quiz →
          </a>
        </div>
      </div>
    </div>
    '''
    text = f'{username} — you scored {score}/{total} ({percentage}%) on {subject_name} {topic_name}. Visit https://zeequiz.co.uk to keep revising.'
    try:
        _send(to_email, subject_line, html, text)
    except Exception as e:
        print(f'[mailer] Failed to send report to {to_email}: {e}')
