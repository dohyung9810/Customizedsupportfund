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
            num_employees = st.number_input("최근 1년 평균 고용보험 피보험자 수는 몇 명입니까?", min_value=0)
            industry = st.selectbox("귀사의 업종은 무엇입니까?", [
                "제조업 (C. 대분류)",
                "지식서비스/문화콘텐츠/신재생에너지 산업",
                "청년 창업기업/미래유망기업/지역주력산업",
                "기타 일반 업종"])
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
        with st.form("청년정보_form"):
            age = st.slider("채용한 청년의 나이는 몇 세입니까? (군필자는 복무기간 고려)", 15, 45, 25)
            is_difficult = st.checkbox("해당 청년은 '취업애로청년' 조건에 해당합니까?")
            over_6m = st.checkbox("청년을 6개월 이상 정규직으로 고용하고 있습니까?")
            over_18m = st.checkbox("청년이 18개월 이상 근속했습니까?")
            submitted2 = st.form_submit_button("✅ 결과 확인하기")

            if submitted2:
                st.session_state.청년정보_data = {
                    "age": age,
                    "is_difficult": is_difficult,
                    "over_6m": over_6m,
                    "over_18m": over_18m
                }
                st.session_state.step = 3
                st.rerun()

    if st.session_state.step == 3:
        st.subheader("3단계: 결과")

        기업 = st.session_state.get("기업정보_data", {})
        청년 = st.session_state.get("청년정보_data", {})

        필수_기업키 = ["excluded", "industry", "num_employees"]
        필수_청년키 = ["age", "is_difficult", "over_6m", "over_18m"]

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

            if 기업["excluded"] == "해당 없음 (정상 기업)" and 청년["age"] <= 39 and 청년["is_difficult"] and 청년["over_6m"]:
                if 기업["num_employees"] >= 5 or 기업["industry"] in [
                    "지식서비스/문화콘텐츠/신재생에너지 산업",
                    "청년 창업기업/미래유망기업/지역주력산업"]:
                    eligible_type1 = True

            if 기업["excluded"] == "해당 없음 (정상 기업)" and 기업["industry"] == "제조업 (C. 대분류)" and 기업["num_employees"] >= 5 and 청년["age"] <= 34 and 청년["over_6m"]:
                eligible_type2 = True

            if eligible_type1 or eligible_type2:
                st.success("✅ 귀사는 청년일자리도약장려금 지원 대상입니다!")
                if eligible_type1:
                    st.markdown("- **유형Ⅰ**: 취업애로청년 채용 시 최대 720만원")
                if eligible_type2:
                    st.markdown("- **유형Ⅱ**: 제조업 등 빈일자리 업종 청년 채용 시 최대 720만원")
                if 청년["over_18m"] and eligible_type2:
                    st.markdown("🎉 18개월 이상 근속 시 **청년 장기근속 인센티브 480만원** 추가 가능!")
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
            st.markdown("- 고용보험과 국민연금 보험료의 **사업주 부담분 80% 지원**")
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

# ▶ 탭 3: 시니어인턴십 참여기업 자가진단
with tabs[2]:
    st.header("시니어인턴십 참여기업 자가진단")
    st.markdown("시니어인턴십 지원사업에 참여 가능한 기업 및 시니어 근로자 여부를 확인합니다.")

    st.subheader("① 참여기업 요건 확인")
    with st.form("시니어기업_form"):
        is_insured = st.checkbox("4대 보험에 가입한 사업장입니까?")
        offers_jobs_to_seniors = st.checkbox("시니어(60세 이상)에게 일자리를 제공합니까?")

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
        eligible_corp = (
            is_insured and offers_jobs_to_seniors and job_title_valid and employment_type_valid and
            industry_type not in ["소비향락 업종", "다단계판매 업체", "임금체불 확정 사업장", "정부 예산지원 사업장"] and
            not is_seasonal and not has_no_continuous_hiring
        )

        if eligible_corp:
            st.success("✅ 귀사는 시니어인턴십 참여 가능한 기업입니다!")
        else:
            st.error("❌ 귀사는 현재 조건으로 시니어인턴십 참여기업 요건을 충족하지 않습니다.")

    st.divider()
    st.subheader("② 시니어 참여자 요건 확인")
    with st.form("시니어근로자_form"):
        senior_age = st.number_input("근로자의 나이를 입력해 주세요.", min_value=0, max_value=100, step=1)
        is_already_employed = st.checkbox("인턴십 시작일 기준 4대보험에 가입되어 있습니까?")
        is_recently_worked_here = st.checkbox("최근 90일 내 이 사업장에 취업한 적이 있습니까?")
        is_already_participated = st.checkbox("같은 해 두 개 이상 사업장의 인턴십에 참여했거나 하고 있습니까?")
        is_family_related = st.checkbox("사업주와 가족(배우자, 직계, 4촌 이내 친족) 관계입니까?")
        is_foreigner = st.checkbox("국내 거주 외국인입니까?")

        submit_senior_worker = st.form_submit_button("✅ 시니어 참여자격 결과 확인")

    if submit_senior_worker:
        eligible_senior = (
            senior_age >= 60 and
            not is_already_employed and
            not is_recently_worked_here and
            not is_already_participated and
            not is_family_related and
            not is_foreigner
        )

        if eligible_senior:
            st.success("✅ 해당 시니어 근로자는 인턴십 참여 대상입니다!")
        else:
            st.error("❌ 해당 시니어 근로자는 인턴십 참여 요건에 부합하지 않습니다.")
