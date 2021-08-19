import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import {MutableRefObject} from "react";

const exportToPdf = (tableRef: MutableRefObject<any>) => {
  html2canvas(tableRef.current, {
    backgroundColor: null,
    scale: 2,
    scrollX: 0,
    scrollY: 0,
  }).then((canvas) => {
    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF('l', 'pt', 'a4', false);

    const imgProps = pdf.getImageProperties(canvas);
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

    pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight, undefined, undefined);

    const date = new Date().toISOString().split('T')[0];
    pdf.save(`ratings-${date}.pdf`);
  });
};

export default exportToPdf;
