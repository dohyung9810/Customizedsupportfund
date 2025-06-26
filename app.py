import streamlit as st

st.set_page_config(page_title="청년일자리도약장려금 & 두루누리 & 시니어인턴십 자가진단", layout="centered")
st.title("💼 고용지원금 자가진단 대시보드")

# 탭 설정
tabs = st.tabs(["청년일자리도약장려금", "두루누리 사회보험료 지원", "시니어인턴십 참여기업 자가진단"])

# ▶ 탭 1: 청년일자리도약장려금
with tabs[0]:
    st.header("청년일자리도약장려금 자가진단")
    st.markdown("이 대시보드는 **사업주**가 청년일자리도약장려금 **지원 대상**인지 단계별로 확인할 수 있도록 돕습니다.")

    if "step" not in st.session_state:
        st.session_state.step = 1
    if "기업정보_data" not in st.session_state:
        st.session_state.기업정보_data = {}
    if "청년정보_data" not in st.session_state:
        st.session_state.청년정보_data = {}

    if st.session_state.step == 1:
        st.subheader("1단계: 기업 정보 입력")
        with st.form("기업정보_form"):
            num_employees = st.number_input("최근 1년 평균 고용보험 가입자 수는 몇 명입니까?", min_value=0)
            industry = st.selectbox("귀사의 업종은 무엇입니까?", [
                "일반 업종",
                "제조업 (C. 대분류)",
                "지식서비스/문화콘텐츠/신재생에너지 산업",
                "청년 창업기업/미래유망기업/지역주력산업",
                ])
            excluded = st.radio("다음 항목 중 하나라도 해당합니까?", [
                "해당 없음 (정상 기업)",
                "소비/향락 업종",
                "임금 체불 명단 포함",
                "중대재해 명단 포함"])
            submitted1 = st.form_submit_button("👉 다음 단계로")

            if submitted1:
                st.session_state.기업정보_data = {
                    "num_employees": num_employees,
                    "industry": industry,
                    "excluded": excluded
                }
                st.session_state.step = 2
                st.rerun()

    if st.session_state.step == 2:
        st.subheader("2단계: 청년 채용 정보")

        with st.expander("💡 '취업애로청년'이란?"):
                st.markdown("""
                    아래 어느 하나에 해당하면 **취업애로청년**에 해당합니다:

                    ❶ **연속하여 4개월** 이상 실업상태인 청년  
                    ❷ **고졸 이하 학력**인 청년  
                    ❸ **국민취업지원제도**에 참여하거나,  
                    ❹ **청년일경험지원사업**을 수료한 후 **최초**로 취업한 청년  
                    ❺ **청년도전지원사업** 수료 청년  
                    ❻ **자영업 폐업** 이후 **최초**로 취업한 청년  
                    ❼ **최종학교 졸업일 이후** 채용일까지 **고용보험 총 가입기간이 12개월 미만**인 청년
                        """)

        with st.form("청년정보_form"):
            age = st.slider("채용한 청년의 만 나이는 몇 세입니까? (군필자는 복무기간 고려)", 15, 45, 25)
            is_difficult = st.checkbox("해당 청년은 '취업애로청년' 조건에 해당합니까?")
            over_6m = st.checkbox("청년을 6개월 이상 정규직으로 고용할 예정인가요?")
            over_28h = st.checkbox("청년의 주당 근로시간이 28시간 이상인가요?")
            # over_18m = st.checkbox("청년이 18개월 이상 근속했습니까?")
            submitted2 = st.form_submit_button("✅ 결과 확인하기")

            if submitted2:
                st.session_state.청년정보_data = {
                    "age": age,
                    "is_difficult": is_difficult,
                    "over_6m": over_6m,
                    "over_28h": over_28h
                }
                st.session_state.step = 3
                st.rerun()

    if st.session_state.step == 3:
        st.subheader("3단계: 결과")

        기업 = st.session_state.get("기업정보_data", {})
        청년 = st.session_state.get("청년정보_data", {})

        필수_기업키 = ["excluded", "industry", "num_employees"]
        필수_청년키 = ["age", "is_difficult", "over_6m", 'over_28h']

        if all(k in 기업 for k in 필수_기업키) and all(k in 청년 for k in 필수_청년키):
            eligible_type1 = False
            eligible_type2 = False
            ineligible_reasons = []

            if 기업["excluded"] != "해당 없음 (정상 기업)":
                ineligible_reasons.append("지원 제외 업종 또는 명단 포함")

            if 기업["num_employees"] < 5 and 기업["industry"] not in [
                "지식서비스/문화콘텐츠/신재생에너지 산업",
                "청년 창업기업/미래유망기업/지역주력산업"]:
                ineligible_reasons.append("5인 미만이며 특례 업종에 해당하지 않음")

            if 기업["excluded"] == "해당 없음 (정상 기업)" and 청년["age"] <= 39 and 청년["is_difficult"] and 청년["over_6m"] and 청년["over_28h"]:
                if 기업["num_employees"] >= 5 or 기업["industry"] in [
                    "지식서비스/문화콘텐츠/신재생에너지 산업",
                    "청년 창업기업/미래유망기업/지역주력산업"]:
                    eligible_type1 = True

            if 기업["excluded"] == "해당 없음 (정상 기업)" and 기업["industry"] == "제조업 (C. 대분류)" and 기업["num_employees"] >= 5 and 청년["age"] <= 34 and 청년["over_6m"]:
                # Q. 주 30시간 이상인 경우도 포함이 되는가?
                eligible_type2 = True

            if eligible_type1 or eligible_type2:
                st.success("✅ 귀사는 청년일자리도약장려금 지원 대상입니다!")

                if eligible_type1:
                    st.markdown("- **유형Ⅰ**: 취업애로청년 채용 시 최대 720만원")
                if eligible_type2:
                    st.markdown("- **유형Ⅱ**: 제조업 등 빈일자리 업종 청년 채용 시 최대 720만원")
                st.info("⚠️ 본 결과는 참고용이며, 최종 판단은 고용노동부의 사업 운영지침에 따릅니다.")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.link_button("📩 DM 문의하기", url="https://www.instagram.com/bunchangman_official/")  # 여기에 실제 링크 입력
                with col2:
                    st.link_button("💬 카카오톡 상담", url="http://pf.kakao.com/_xgRTan/chat")     # 여기에 실제 링크 입력
                with col3:
                    if st.button("🔄 처음으로 돌아가기"):
                        st.session_state.step = 1
                        st.session_state.기업정보_data = {}
                        st.session_state.청년정보_data = {}
                        st.rerun()

                # 담당자 안내 (주석 처리)
                # (권연진 본부장 / Tel. 02-527-0935 / 010-9359-6401)
                # (최은실 파트장 / Tel. 02-527-0922 / 010-2270-2022)
            else:
                st.error("❌ 현재 조건으로는 지원 대상이 아닙니다.")
                st.markdown("**이유:**")
                for reason in ineligible_reasons:
                    st.markdown(f"- {reason}")

                st.info("⚠️ 본 결과는 참고용이며, 최종 판단은 고용노동부의 사업 운영지침에 따릅니다.")
                if st.button("🔄 처음으로 돌아가기"):
                        st.session_state.step = 1
                        st.session_state.기업정보_data = {}
                        st.session_state.청년정보_data = {}
                        st.rerun()
            

        else:
            st.warning("⚠️ 필수 정보가 누락되었습니다. 처음부터 다시 진행해 주세요.")
            if st.button("🔄 처음으로 돌아가기"):
                st.session_state.step = 1
                st.rerun()

# ▶ 탭 2: 두루누리 지원
with tabs[1]:
    st.header("두루누리 사회보험료 지원 자가진단")
    st.markdown("신규 가입자에게 고용보험과 국민연금 보험료의 일부를 지원하는 제도입니다.")

    with st.form("두루누리"):
        worker_count = st.number_input("귀사의 근로자 수(1~9명 대상)", min_value=1, max_value=100, step=1)
        is_new = st.radio("해당 근로자는 최근 6개월간 고용보험·국민연금 자격취득 이력이 없습니까?", ["예", "아니오"])
        avg_monthly_wage = st.number_input("해당 근로자의 월평균 보수 (단위: 원)", min_value=0)

        submit_duru = st.form_submit_button("✅ 두루누리 지원 대상 여부 확인")

    if submit_duru:
        if worker_count <= 9 and is_new == "예" and avg_monthly_wage <= 2700000:
            st.success("✅ 해당 근로자는 두루누리 사회보험료 지원 대상입니다!")
            st.markdown("- 고용보험과 국민연금 보험료의 **사업주, 근로자 부담분 80% 지원**")

            col1, col2 = st.columns(2)
            with col1:
                st.link_button("📩 DM 문의하기", url="https://www.instagram.com/bunchangman_official/")  # 여기에 실제 링크 입력
            with col2:
                st.link_button("💬 카카오톡 상담", url="http://pf.kakao.com/_xgRTan/chat")     # 여기에 실제 링크 입력

        else:
            st.error("❌ 해당 근로자는 두루누리 지원 대상이 아닙니다.")
            st.markdown("**검토 항목:**")
            if worker_count > 9:
                st.markdown("- 근로자 수가 10명 이상")
            if is_new != "예":
                st.markdown("- 최근 6개월간 고용보험/국민연금 가입 이력 있음")
            if avg_monthly_wage > 2700000:
                st.markdown("- 월평균 보수가 270만원 초과")

    st.caption("문의: 근로복지공단 1588-0075 / 국민연금공단 1355")

with tabs[2]:
    st.header("시니어인턴십 참여기업 자가진단")
    st.markdown("시니어인턴십 지원사업에 참여 가능한 기업 및 시니어 근로자 여부를 확인합니다.")

    st.subheader("① 참여기업 요건 확인")
    with st.form("시니어기업_form"):
        is_insured = st.checkbox("4대 보험에 가입한 사업장입니까?")
        offers_jobs_to_seniors = st.checkbox("시니어(60세 이상)에게 일자리 제공할 예정인가요?")

        industry_type = st.selectbox("귀사의 업종 형태는 무엇입니까?", [
            "일반 기업",
            "비영리민간단체",
            "소비향락 업종",
            "다단계판매 업체",
            "임금체불 확정 사업장",
            "정부 예산지원 사업장",
            "기타"])

        is_seasonal = st.checkbox("3개월 미만의 계절수요 업체입니까?")
        has_no_continuous_hiring = st.checkbox("최근 2년간 인턴 고용 실적이 전혀 없습니까?")
        job_title_valid = st.checkbox("채용하려는 직무는 제한 직종(룸메이드, 간병인 등)에 해당하지 않습니까?")
        employment_type_valid = st.checkbox("채용 형태가 일용직·건설일용직·파견직이 아닙니까?")

        submit_senior_corp = st.form_submit_button("✅ 기업 참여자격 결과 확인")

    if submit_senior_corp:
        # 기업 불충족 항목 수집
        failed_reqs = []
        if not is_insured:
            failed_reqs.append("4대 보험에 미가입된 사업장입니다.")
        if not offers_jobs_to_seniors:
            failed_reqs.append("시니어(60세 이상) 일자리 제공 계획이 없습니다.")
        if industry_type in ["소비향락 업종", "다단계판매 업체", "임금체불 확정 사업장", "정부 예산지원 사업장"]:
            failed_reqs.append(f"제외 대상 업종: {industry_type}")
        if is_seasonal:
            failed_reqs.append("3개월 미만의 계절수요 업체입니다.")
        if has_no_continuous_hiring:
            failed_reqs.append("최근 2년간 인턴 고용 실적이 있습니다.")
        if not job_title_valid:
            failed_reqs.append("제한 직종(룸메이드, 간병인 등)에 해당합니다.")
        if not employment_type_valid:
            failed_reqs.append("일용직·건설일용직·파견직 형태입니다.")

        if not failed_reqs:
            st.success("✅ 귀사는 시니어인턴십 참여 가능한 기업입니다!")
            col1, col2 = st.columns(2)
            with col1:
                st.link_button("📩 DM 문의하기", url="https://www.instagram.com/bunchangman_official/")  # 여기에 실제 링크 입력
            with col2:
                st.link_button("💬 카카오톡 상담", url="http://pf.kakao.com/_xgRTan/chat")     # 여기에 실제 링크 입력
        else:
            st.error("❌ 아래 조건을 충족하지 않아 참여기업 요건에서 제외되었습니다:")
            for msg in failed_reqs:
                st.write(f"- {msg}")

    st.divider()
    st.subheader("② 시니어 참여자 요건 확인")
    with st.form("시니어근로자_form"):
        senior_age = st.number_input("근로자의 나이를 입력해 주세요.", min_value=0, max_value=200, step=1)
        is_already_employed = st.checkbox("인턴십 시작일 기준 4대보험에 가입되어 있습니까?")
        is_recently_worked_here = st.checkbox("최근 90일 내 이 사업장에 취업한 적이 있습니까?")
        is_already_participated = st.checkbox("같은 해 두 개 이상 사업장의 인턴십에 참여했거나 하고 있습니까?")
        is_family_related = st.checkbox("사업주와 가족(배우자, 직계, 4촌 이내 친족) 관계입니까?")
        is_insured_ind = st.checkbox("인턴십 참여시작일 기준 이미 4대 보험 자격을 취득 중인가요?")

        submit_senior_worker = st.form_submit_button("✅ 시니어 참여자격 결과 확인")

    if submit_senior_worker:
        # 근로자 불충족 항목 수집
        failed_reqs = []
        if senior_age < 60:
            failed_reqs.append(f"나이 {senior_age}세로, 60세 이상이 아닙니다.")
        if is_already_employed:
            failed_reqs.append("인턴십 시작일 기준 이미 4대보험에 가입된 상태입니다.")
        if is_recently_worked_here:
            failed_reqs.append("최근 90일 내에 동일 사업장에 취업한 적이 있습니다.")
        if is_already_participated:
            failed_reqs.append("같은 해 두 개 이상의 사업장 인턴십에 참여했습니다.")
        if is_family_related:
            failed_reqs.append("사업주와 가족 관계입니다.")
        if is_insured_ind:
            failed_reqs.append("인턴십 참여 시작일에 이미 4대 보험 자격을 취득 중입니다.")

        if not failed_reqs:
            st.success("✅ 해당 시니어 근로자는 인턴십 참여 대상입니다!")
            col1, col2 = st.columns(2)
            with col1:
                st.link_button("📩 DM 문의하기", url="https://www.instagram.com/bunchangman_official/")  # 여기에 실제 링크 입력
            with col2:
                st.link_button("💬 카카오톡 상담", url="http://pf.kakao.com/_xgRTan/chat")     # 여기에 실제 링크 입력
        else:
            st.error("❌ 아래 조건을 충족하지 않아 참여자격에서 제외되었습니다:")
            for msg in failed_reqs:
                st.write(f"- {msg}")
