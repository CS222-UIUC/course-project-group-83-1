const header = document.querySelector(".header");
const obs = new IntersectionObserver(
    function (entries) {
        const ent = entries[0];
        if (ent.isIntersecting) {
            document.body.classList.remove("sticky");
        } else {
            document.body.classList.add("sticky");
        }
    }, {
    root: null,
    threshold: 0,
    rootMargin: "-80px"
}
);
obs.observe(header);