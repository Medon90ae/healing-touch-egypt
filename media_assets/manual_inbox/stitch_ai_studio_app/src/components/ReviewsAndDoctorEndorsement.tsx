import React from 'react';
import { Award, Star, CheckCircle, Quote, MapPin } from 'lucide-react';
import { Campaign } from '../types/campaign';

interface ReviewsAndDoctorEndorsementProps {
  campaign: Campaign;
}

export const ReviewsAndDoctorEndorsement: React.FC<ReviewsAndDoctorEndorsementProps> = ({ campaign }) => {
  const { doctorEndorsement, reviews } = campaign;

  return (
    <section className="py-12 sm:py-16 bg-[#FBFDFB] border-b border-[#E2ECE6]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Doctor Clinical Endorsement Section */}
        <div className="bg-gradient-to-br from-[#064E3B] to-[#003527] text-white rounded-3xl p-6 sm:p-10 shadow-xl mb-12 relative overflow-hidden">
          {/* Subtle medical watermark */}
          <div className="absolute top-0 right-0 w-80 h-80 bg-white/5 rounded-full blur-2xl pointer-events-none" />

          <div className="relative grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            <div className="lg:col-span-8 space-y-4">
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 backdrop-blur-sm text-[#82F5C1] text-xs font-semibold border border-white/15">
                <Award className="w-4 h-4" />
                <span>{doctorEndorsement.seal}</span>
              </div>

              <div className="relative">
                <Quote className="w-10 h-10 text-white/15 absolute -top-4 -right-4 -z-0" />
                <p className="text-base sm:text-xl font-medium text-white leading-relaxed z-10 relative">
                  "{doctorEndorsement.statement}"
                </p>
              </div>

              <div className="pt-2 border-t border-white/15">
                <div className="font-bold text-base sm:text-lg text-[#82F5C1]">
                  {doctorEndorsement.doctorName}
                </div>
                <div className="text-xs sm:text-sm text-white/90">
                  {doctorEndorsement.title}
                </div>
                <div className="text-xs text-[#95D3BA]">
                  {doctorEndorsement.hospital}
                </div>
              </div>
            </div>

            <div className="lg:col-span-4 flex flex-col items-center justify-center p-6 bg-white/5 backdrop-blur-md rounded-2xl border border-white/10 text-center">
              <div className="w-16 h-16 rounded-full bg-[#82F5C1]/20 border border-[#82F5C1]/40 flex items-center justify-center text-[#82F5C1] mb-3">
                <CheckCircle className="w-8 h-8" />
              </div>
              <div className="font-bold text-sm text-white mb-1">
                اعتماد الأطباء المصريين
              </div>
              <p className="text-xs text-white/80 max-w-xs">
                مطابق لأحدث إرشادات الجمعيات الطبية للجراحة التجميلية والعناية بالجروح
              </p>
            </div>
          </div>
        </div>

        {/* Patient Reviews Section */}
        <div className="text-center max-w-3xl mx-auto mb-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#E6EEFF] text-[#003527] text-xs sm:text-sm font-semibold mb-3 border border-[#D0DBED]">
            <Star className="w-4 h-4 text-[#D97706] fill-[#D97706]" />
            <span>تجارب المرضى والأمهات الموثقة</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-[#003527] mb-2">
            نتائج حقيقية لمرضانا في مختلف المحافظات
          </h2>
          <p className="text-sm text-[#404944]">
            قصص تعافٍ مطمئنة تؤكد فاعلية البروتوكول الطبي في منع الندبات وتسريع الشفاء.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {reviews.map((rev, idx) => (
            <div
              key={idx}
              className="bg-white rounded-2xl border border-[#E2ECE6] p-6 shadow-xs flex flex-col justify-between"
            >
              <div>
                {/* Rating Stars */}
                <div className="flex items-center gap-1 mb-3">
                  {[...Array(rev.stars)].map((_, i) => (
                    <Star key={i} className="w-4 h-4 text-[#D97706] fill-[#D97706]" />
                  ))}
                  <span className="text-xs text-[#707974] mr-2">{rev.timeAgo}</span>
                </div>

                <p className="text-xs sm:text-sm text-[#121C2A] leading-relaxed mb-4">
                  "{rev.comment}"
                </p>
              </div>

              <div className="pt-3 border-t border-[#E2ECE6] flex items-center justify-between">
                <div>
                  <div className="font-bold text-xs text-[#003527] flex items-center gap-1">
                    <span>{rev.author}</span>
                    {rev.verified && (
                      <span className="text-[10px] bg-[#E6EEFF] text-[#059669] px-1.5 py-0.2 rounded font-semibold">
                        طلب موثق
                      </span>
                    )}
                  </div>
                  <div className="text-[11px] text-[#707974] flex items-center gap-1 mt-0.5">
                    <MapPin className="w-3 h-3 text-[#059669]" />
                    <span>{rev.location}</span>
                  </div>
                </div>

                <span className="text-[10px] text-[#404944] bg-[#F3F7F5] px-2 py-1 rounded">
                  {rev.procedure}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
