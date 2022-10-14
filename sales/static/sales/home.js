const reportBtn = document.getElementById('report-btn')
const img = document.getElementById('img')
const modalBody = document.getElementById('modal-body')
const reportForm = document.getElementById('report-form')
const alertBox = document.getElementById('alert-box')
const alertBoxCSV = document.getElementById('csv-alert-box')

const reportName = document.getElementById('id_name')
const reportRemarks = document.getElementById('id_remarks')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0]
const csv_btn = document.getElementById("btn_to_csv")
const csv_table = document.getElementById("table_to_csv")

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
    `
}

const handleCSVAlerts = (type, msg) => {
    alertBoxCSV.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
    `
}

if (img){
    reportBtn.classList.remove('not-visible')
}

reportBtn.addEventListener('click', ()=>{
    console.log('clicked')
    img.setAttribute('class', 'w-100')
    //append ==> add the end of object  
    //prepend ==> add the first of object
    modalBody.prepend(img)

    console.log(img.src)

    reportForm.addEventListener('submit', e=>{
        //   للصفحة refresh يقوم بتنفيذ الحدث قبل عمل  e.preventDefault()
        e.preventDefault()               
        const formData = new FormData()
        formData.append('csrfmiddlewaretoken', csrf.value)
        formData.append('name', reportName.value)
        formData.append('remarks', reportRemarks.value)
        formData.append('image', img.src)

        $.ajax({
            type: 'POST',
            url: '/reports/save/',
            data: formData,
            success: function(response){
                console.log(response)
                handleAlerts('success', 'report created')
                reportForm.reset()
            },
            error: function(error){
                console.log(error)
                handleAlerts('danger', 'ups... something went wrong')
            },
            processData: false,
            contentType: false,
        })
    })
})





csv_btn.addEventListener('click',  ()=>{

    const formData = {'data': csv_table.value}

    $.ajax({
        type: 'POST',
        url:'/to_csv/',
        data: formData,
        success: function(){
           handleCSVAlerts('success', 'CSV file has been created in your desktop')
            console.log('success')

        },
        error: function(){
            handleCSVAlerts('danger', 'ups... something went wrong')
            console.log('danger')
        },

    })

})