// ContactUs.js
import React from 'react';

function ContactUs() {
    return (
        <div>
            <h1>Contact Us</h1>
            <p>We’d love to hear from you!</p>
            <p>Email: support@dropstop.com</p>
            <p>Phone: +123-456-7890</p>
            <form>
                <label>
                    Your Name:
                    <input type="text" name="name" />
                </label>
                <br />
                <label>
                    Your Message:
                    <textarea name="message" />
                </label>
                <br />
                <button type="submit">Submit</button>
            </form>
        </div>
    );
}

export default ContactUs;
