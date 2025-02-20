function sendMail() {
    let params = {
        name:'keentech2019@gmail.com',
        to_name:'lalitgarg2005@gmail.com',
        reply_to:'lalitgarg2005@gmail.com',
        subject:'Job Application',
        message: 'ou have Successfully applied to the job.',

    }

    emailjs.send('service_rzkct4r', 'template_w1o0j1b', params).then(alert('Email Sent Successfully'));

}