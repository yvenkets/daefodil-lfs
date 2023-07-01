!(function (o) {
    o.fn.contentZoomSlider = function (n) {
        let t = o(this),
            e = ".ranger",
            i = o.extend({ toolContainer: "#tool-container", setp: 25, min: 25, max: 150, zoom: 100 }, n);
        function a() {
            let o = parseFloat(t.css("zoom"));
            return o || (o = 1), o;
        }
        function l(n) {
            t.css("-moz-transform", `scale(${n}`), t.css("transform-origin", "50%,0"), t.css({ zoom: n }), o(`${i.toolContainer} ${e}`).val(n), o(`${i.toolContainer} .zoom-value`).text((100 * n).toFixed(0) + "%");
        }
        o(i.toolContainer).html(
            `<div class="row">\n            <div class="col-sm-12 text-center zoominout" style="position: fixed; width:20%; bottom: 20px; right: 34%; background-color: #64748B; padding: 10px 15px 10px 15px; border-radius: 4px;">\n                <span style="float: right; color: #fff;" class="zoom-value">${
                i.zoom
            }%</span>\n                <a href="#" title="Zoom Out" class="zoom-out"> <i style="color: white; font-size: 12px; border: 2px solid #ffff; border-radius: 50%; padding: 3px;" class="fa fa-minus m-1"></i> </a>\n                <input class="mb-1 ranger" type="range" style="transform: translateY(4px); accent-color: #fff;" value="${i.zoom / 100}" step="${i.setp / 100}" min="${
                i.min / 100
            }" max="${i.max / 100}" />\n                <a href="#" title="Zoom In" class="zoom-in"> <i style="color: white; font-size: 12px; border: 2px solid #ffff; border-radius: 50%; padding: 3px;" class="fa fa-plus m-1"></i></a>\n     </div>\n        </div>`
        ),
            o(document)
                .off("click", `${i.toolContainer} .zoom-out`)
                .on("click", `${i.toolContainer} .zoom-out`, function () {
                    !(function () {
                        let o = a();
                        o > i.min / 100 && l(o - i.setp / 100);
                    })();
                }),
            o(document)
                .off("click", `${i.toolContainer} .zoom-in`)
                .on("click", `${i.toolContainer} .zoom-in`, function () {
                    !(function () {
                        let o = a();
                        o < i.max / 100 && l(o + i.setp / 100);
                    })();
                }),
            o(document)
                .off("mousemove", `${i.toolContainer} ${e}`)
                .on("mousemove", `${i.toolContainer} ${e}`, function () {
                    l(parseFloat(o(`${i.toolContainer} ${e}`).val()));
                }),
            l(i.zoom / 100);
    };
})(jQuery);
