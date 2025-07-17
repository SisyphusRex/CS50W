let counter = 0;
            
function count() {
    const heading = document.querySelector('h1');
    counter++;
    heading.innerHTML = counter;

    if (counter % 10 === 0) {
        alert(`Count is now ${counter}`);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('button').onclick = count;
})