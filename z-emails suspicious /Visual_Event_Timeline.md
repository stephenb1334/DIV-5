<style>
    .timeline-container {
        font-family: 'Lato', Arial, sans-serif;
        max-width: 900px;
        margin: 40px auto;
        color: #333;
    }
    .timeline-header {
        text-align: center;
        margin-bottom: 40px;
    }
    .timeline-header h1 {
        font-size: 2.5em;
        color: #004261;
    }
    .timeline-card {
        background-color: #ffffff;
        border-left: 5px solid #009fc7;
        padding: 20px 30px;
        margin: 20px 0;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .timeline-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .timeline-card.key-event {
        border-left-color: #D0021B;
    }
    .timeline-date {
        font-weight: bold;
        font-size: 1.2em;
        color: #004261;
        margin-bottom: 10px;
    }
    .timeline-title {
        font-size: 1.4em;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .timeline-description {
        font-size: 1em;
        line-height: 1.6;
    }
    .timeline-description code {
        background-color: #f0f0f0;
        padding: 2px 5px;
        border-radius: 4px;
        font-family: monospace;
    }
    .icon {
        font-size: 1.5em;
        margin-right: 10px;
        vertical-align: middle;
    }
</style>

<div class="timeline-container">
    <div class="timeline-header">
        <h1>Timeline of Account Events</h1>
    </div>

    <!-- Event 1 -->
    <div class="timeline-card">
        <div class="timeline-date">February 15, 2025</div>
        <div class="timeline-title"><span class="icon">📧</span>Baseline: Direct Communication</div>
        <div class="timeline-description">
            Mr. Cooper sends a payment confirmation email <b>directly</b> to <code>stephen.boerner@gmail.com</code>. This proves Stephen's personal email was a known, primary contact for the account. No forwarding was involved.
        </div>
    </div>

    <!-- Event 2 -->
    <div class="timeline-card">
        <div class="timeline-date">March 20 & June 2, 2025</div>
        <div class="timeline-title"><span class="icon">🚫</span>Forwarding Disabled</div>
        <div class="timeline-description">
            Test emails sent to the shared account, <code>stephenandmelissaboerner@gmail.com</code>, are <b>not</b> forwarded. This indicates the automatic forwarding rule was manually turned off during these periods, preventing Stephen from seeing incoming mail.
        </div>
    </div>

    <!-- Event 3 - Key Event -->
    <div class="timeline-card key-event">
        <div class="timeline-date">May 2, 2025</div>
        <div class="timeline-title"><span class="icon">🔧</span>Key Event: Unilateral Account Changes</div>
        <div class="timeline-description">
            On this day, the forwarding rule was inexplicably active. This led to the discovery of two key actions taken by Melissa Bemer:
            <br><br>
            <ol>
                <li><b>(15:55 UTC) New Profile Creation:</b> An email is sent to activate a new, separate online profile for the joint account under the name "Melissa Bemer" and tied to her personal email.</li>
                <li><b>(15:56 UTC) Contact Email Changed:</b> A confirmation email is sent stating that the contact address was changed from the shared <code>stephenandmelissaboerner@gmail.com</code> to <code>melissabemer@gmail.com</code>.</li>
            </ol>
        </div>
    </div>

    <!-- Event 4 -->
    <div class="timeline-card">
        <div class="timeline-date">May 2, 2025</div>
        <div class="timeline-title"><span class="icon">💡</span>Discovery via Technical Oversight</div>
        <div class="timeline-description">
            The only reason these actions were discovered by Stephen is that the forwarding rule from the shared account to his personal account was active. The evidence of the changes was automatically and unintentionally delivered to him.
        </div>
    </div>

</div>