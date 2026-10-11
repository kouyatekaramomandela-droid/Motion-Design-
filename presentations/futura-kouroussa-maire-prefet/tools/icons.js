// Pictogrammes (Font Awesome 5 via react-icons) rendus en PNG 256 px, blancs ou bleu nuit, pour les pastilles.
const React = require("react");
const { renderToStaticMarkup } = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");
const ICONS = {
  capter: "FaHandHoldingUsd", gerer: "FaLock", redistribuer: "FaHandHoldingHeart",
  deputes: "FaLandmark", visham: "FaHandshake", apedk: "FaUsers",
  mairie: "FaBuilding", prefecture: "FaUniversity", bouclier: "FaShieldAlt", check: "FaCheck",
  front: "FaUsers", negocier: "FaBalanceScale", contrat: "FaFileSignature", livrer: "FaTint",
  routes: "FaRoad", eau: "FaTint", sante: "FaHeartbeat", education: "FaGraduationCap",
  agriculture: "FaSeedling", emploi: "FaBriefcase", femmes: "FaFemale", electricite: "FaBolt",
};
(async () => {
  for (const [name, comp] of Object.entries(ICONS)) {
    for (const [suffix, color] of [["", "#FFFFFF"], ["-nuit", "#12264A"]]) {
      const svg = renderToStaticMarkup(React.createElement(fa[comp], { size: 256, color }));
      await sharp(Buffer.from(svg)).resize(256, 256, { fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } })
        .png().toFile(`assets/icons/${name}${suffix}.png`);
    }
  }
  console.log("icons", Object.keys(ICONS).length);
})();
