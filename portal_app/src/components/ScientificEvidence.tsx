import React from 'react';
import { 
  Award, 
  FlaskConical, 
  ExternalLink, 
  CheckCircle, 
  FileCheck2, 
  TrendingUp, 
  Users,
  ShieldAlert
} from 'lucide-react';
import { EvidenceStudy } from '../types/campaign';
import { useInView } from '../hooks/useInView';

interface ScientificEvidenceProps {
  studies: EvidenceStudy[];
  campaignName: string;
}

export const ScientificEvidence: React.FC<ScientificEvidenceProps> = ({
  studies,
  campaignName
}) => {
  const { ref, isInView } = useInView();

  return (
    <section
      id="scientific-evidence"
      ref={ref}
      className="py-12 sm:py-16 bg-[#F8F9FF] border-b border-[#E2ECE6]"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div
          className={`text-center max-w-3xl mx-auto mb-10 transition-all duration-500 ${
            isInView ? 'animate-fade-in-up opacity-100' : 'opacity-0 translate-y-4'
          }`}
        >
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#E6EEFF] text-[#003527] text-xs sm:text-sm font-semibold mb-3 border border-[#D0DBED]">
            <FlaskConical className="w-4 h-4 text-[#059669]" />
            <span>الطب القائم على الدليل (Evidence-Based Medicine)</span>
          </div>
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-[#003527] mb-3">
            دراسات إكلينيكية محكمة وتجارب عشوائية منضبطة
          </h2>
          <p className="text-sm sm:text-base text-[#404944]">
            لا نعتمد على الوعود التسويقية؛ جميع مكونات بروتوكول {campaignName} مستندة لأبحاث منشورة في أكبر الدوريات الجراحية العالمية (PubMed وCochrane Library وFDA).
          </p>
        </div>

        {/* Top Key Statistical Indicators Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-5 mb-10">
          <div className="bg-white p-4 sm:p-5 rounded-2xl border border-[#E2ECE6] shadow-xs text-center">
            <div className="text-2xl sm:text-3xl font-extrabold text-[#059669] mb-1">
              86%
            </div>
            <div className="text-xs sm:text-sm font-bold text-[#003527] mb-0.5">
              تسطيح ووقاية من الكلويد
            </div>
            <div className="text-[11px] text-[#707974]">
              وفقاً لمراجعة كوكرين المنهجية
            </div>
          </div>

          <div className="bg-white p-4 sm:p-5 rounded-2xl border border-[#E2ECE6] shadow-xs text-center">
            <div className="text-2xl sm:text-3xl font-extrabold text-[#003527] mb-1">
              100%
            </div>
            <div className="text-xs sm:text-sm font-bold text-[#003527] mb-0.5">
              عزل تام للماء والبكتيريا
            </div>
            <div className="text-[11px] text-[#707974]">
              أغشية بولي يوريثان نصف منفذة
            </div>
          </div>

          <div className="bg-white p-4 sm:p-5 rounded-2xl border border-[#E2ECE6] shadow-xs text-center">
            <div className="text-2xl sm:text-3xl font-extrabold text-[#D97706] mb-1">
              74%
            </div>
            <div className="text-xs sm:text-sm font-bold text-[#003527] mb-0.5">
              تلاشي الحكة والشد المؤلم
            </div>
            <div className="text-[11px] text-[#707974]">
              خلال أول 14 يوماً من الاستخدام
            </div>
          </div>

          <div className="bg-white p-4 sm:p-5 rounded-2xl border border-[#E2ECE6] shadow-xs text-center">
            <div className="text-2xl sm:text-3xl font-extrabold text-[#006C4A] mb-1">
              +40
            </div>
            <div className="text-xs sm:text-sm font-bold text-[#003527] mb-0.5">
              تجربة سريرية عالمية
            </div>
            <div className="text-[11px] text-[#707974]">
              مسجلة في المكتبة القومية للطب
            </div>
          </div>
        </div>

        {/* Desktop Evidence Table */}
        <div className="hidden lg:block bg-white rounded-2xl border border-[#E2ECE6] shadow-sm overflow-hidden mb-8">
          <div className="overflow-x-auto">
            <table className="w-full text-right border-collapse">
              <thead>
                <tr className="bg-[#F3F7F5] border-b border-[#E2ECE6] text-[#003527] text-xs font-bold uppercase tracking-wider">
                  <th className="py-4 px-5">الدراسة والدورية العلمية</th>
                  <th className="py-4 px-4">الإجراء الطبي</th>
                  <th className="py-4 px-4">حجم العينة</th>
                  <th className="py-4 px-5">النتيجة السريرية المثبتة</th>
                  <th className="py-4 px-4 text-center">المؤشر الإحصائي</th>
                  <th className="py-4 px-4 text-center">الاعتماد الدولي</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E2ECE6] text-xs sm:text-sm text-[#404944]">
                {studies.map((study) => (
                  <tr key={study.id} className="hover:bg-[#F8F9FF] transition-colors">
                    {/* Source & Journal */}
                    <td className="py-4 px-5">
                      <div className="font-bold text-[#003527] text-sm mb-1">
                        {study.source}
                      </div>
                      <div className="text-xs text-[#707974] italic">
                        {study.journal}
                      </div>
                    </td>

                    {/* Procedure */}
                    <td className="py-4 px-4">
                      <span className="font-medium text-[#121C2A]">
                        {study.procedure}
                      </span>
                    </td>

                    {/* Sample Size */}
                    <td className="py-4 px-4 whitespace-nowrap">
                      <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-[#EFF4FF] text-[#003527] font-semibold text-xs border border-[#DEE9FC]">
                        <Users className="w-3.5 h-3.5 text-[#059669]" />
                        <span>{study.sampleSize}</span>
                      </div>
                    </td>

                    {/* Finding */}
                    <td className="py-4 px-5 max-w-sm">
                      <p className="text-xs sm:text-sm text-[#121C2A] leading-relaxed">
                        {study.finding}
                      </p>
                    </td>

                    {/* Stat Highlight */}
                    <td className="py-4 px-4 text-center whitespace-nowrap">
                      <span className="inline-block px-3 py-1.5 rounded-full bg-[#E6EEFF] text-[#003527] font-bold text-xs border border-[#82F5C1]">
                        {study.statHighlight}
                      </span>
                    </td>

                    {/* PMID and Grade */}
                    <td className="py-4 px-4 text-center whitespace-nowrap">
                      <div className="space-y-1">
                        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[11px] font-mono font-semibold bg-[#F3F7F5] text-[#003527] border border-[#E2ECE6]">
                          <FileCheck2 className="w-3 h-3 text-[#059669]" />
                          {study.pmid}
                        </span>
                        <div className="text-[10px] font-bold text-[#059669]">
                          {study.evidenceGrade}
                        </div>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Mobile / Tablet Responsive Cards */}
        <div className="lg:hidden space-y-4 mb-8">
          {studies.map((study) => (
            <div
              key={study.id}
              className="p-5 rounded-2xl bg-white border border-[#E2ECE6] shadow-xs space-y-3"
            >
              <div className="flex items-start justify-between gap-2">
                <div>
                  <h3 className="font-bold text-sm text-[#003527]">
                    {study.source}
                  </h3>
                  <div className="text-xs text-[#707974] italic">
                    {study.journal}
                  </div>
                </div>
                <span className="text-[11px] font-mono font-semibold px-2 py-0.5 rounded bg-[#F3F7F5] text-[#003527] border border-[#E2ECE6]">
                  {study.pmid}
                </span>
              </div>

              <div className="flex flex-wrap items-center gap-2 text-xs">
                <span className="px-2.5 py-1 rounded bg-[#EFF4FF] text-[#003527] font-semibold border border-[#DEE9FC]">
                  {study.sampleSize}
                </span>
                <span className="px-2.5 py-1 rounded bg-[#E6EEFF] text-[#003527] font-bold border border-[#82F5C1]">
                  {study.statHighlight}
                </span>
                <span className="text-[11px] font-bold text-[#059669]">
                  {study.evidenceGrade}
                </span>
              </div>

              <div className="text-xs text-[#121C2A] leading-relaxed pt-1 border-t border-[#E2ECE6]">
                <span className="font-semibold text-[#003527]">النتيجة السريرية: </span>
                {study.finding}
              </div>
            </div>
          ))}
        </div>

        {/* Clinical Disclaimer Note */}
        <div className="p-4 rounded-xl bg-white border border-[#E2ECE6] flex items-center justify-between gap-3 text-xs text-[#707974]">
          <div className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-[#059669] shrink-0" />
            <span>
              جميع الدراسات المذكورة معتمدة بالمكتبة القومية الأمريكية للطب (PubMed / NCBI) ومصنفة بدرجة موثوقية عالية (Grade A - Randomized Clinical Trials).
            </span>
          </div>
          <span className="hidden sm:inline font-mono text-[11px] text-[#003527] bg-[#F3F7F5] px-2 py-1 rounded border border-[#E2ECE6]">
            NCBI / Cochrane Database Verified
          </span>
        </div>
      </div>
    </section>
  );
};
