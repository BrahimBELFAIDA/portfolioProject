-- creating a view to store continents data for later use (for the view to show on microsoft ssms you should create the view in a separate querry)

create view vaccinData as
select dea.location, dea.date, population , vac.new_vaccinations, sum(vac.new_vaccinations) over (partition by dea.location order by dea.date) as cumulVaccinations
from portfolioProject..CovidDeaths dea
join portfolioProject..CovidVaccinations vac
on dea.location=vac.location and dea.date=vac.date
where dea.continent is not null

drop view if exists continentData
------------------------------------------------------------------------

select *
from portfolioProject..covidDeaths
order by 3,4 --colonnes correspondants à location et date

select *
from portfolioProject.dbo.CovidVaccinations
order by 3 desc,4 asc

--Selection des données à utiliser 
select location, date,total_cases, new_cases, total_deaths, population 
from portfolioProject.dbo.covidDeaths
order by 1,2

-- total cases and deaths by country
select location,max(total_cases) Cases, max(total_deaths) Deaths
from portfolioProject..CovidDeaths
group by location
order by location

-- toatal cases and deaths, death percentage 

select location, date, total_cases , total_deaths, (total_deaths/total_cases)*100
from portfolioProject..covidDeaths
where location= 'morocco'
order by 1,2

--total cases vs population, show the percentage of infected people in morocco
select location, date, population, total_cases ,  (total_cases/population)*100 infectionPercentage
from portfolioProject..covidDeaths
where location= 'morocco'
order by 1,2

-- countries with the highest infection rate compared to population
select location, population, max(total_cases) as TheTotalcases ,  max(total_cases)/population*100  as infectionPercentage
from portfolioProject..covidDeaths
group by population, location 
order by infectionPercentage desc

-- countries with the highest death percentage 
select location,  max(total_deaths) as deathCount ,  max(total_deaths)/population*100  as deathPercentage
from portfolioProject..covidDeaths
where continent is not null --since otherwise the result is also shown for entire continent ( lines with continent in null and location is europe or asia..)
group by location, population 
order by deathCount desc

-- countinents with the highest death count
select location,  max(total_deaths) as deathCount 
from portfolioProject..covidDeaths
where continent is null -- continent in null in our database where the location is an actual continent
group by location, population 
order by deathCount desc
-- or we can do it by each country's continent
select continent, sum(new_deaths) as deathCount
from portfolioProject..CovidDeaths
where continent is not null
group by  continent 
order by deathCount desc

--global numbers  
select  sum(new_cases) as worldTotalCases, sum(new_deaths) as worldDeathCount, sum(new_deaths)/sum(new_cases)*100 as deathPercentage
from portfolioProject..CovidDeaths
where continent is not null 

-- or for detail by date
select date, sum(new_cases) as worldTotalCases, sum(new_deaths) as worldDeathCount, sum(new_deaths)/sum(new_cases)*100 as deathPercentage
from portfolioProject..CovidDeaths
where continent is not null 
group by date
order by date


--essai de cumulative sum
select location, date,total_cases, new_cases, sum(new_cases) over (order by total_cases) as cumulativecases
from portfolioProject.dbo.covidDeaths
where location like 'afgha%'


--join the tables on location and date (these two constitute a primary key)
select *
from portfolioProject..CovidDeaths dea
join portfolioProject..CovidVaccinations vac
on dea.location=vac.location and dea.date=vac.date
order by 3,4

-- total vaccination vs population , here i can use a cummulaive sum for every country instead of total_vaccinations column
select dea.location, dea.date, population , vac.new_vaccinations, sum(vac.new_vaccinations) over (partition by dea.location order by dea.date) as cumulVaccinations
from portfolioProject..CovidDeaths dea
join portfolioProject..CovidVaccinations vac
on dea.location=vac.location and dea.date=vac.date
where dea.continent is not null and dea.location ='algeria'
order by 1,2

-- total vaccination percentage vs population (using cte)
with popVac (country, date, population, newvac, cumulVacc) 
as  
(select dea.location, dea.date, population , vac.new_vaccinations, sum(vac.new_vaccinations) over (partition by dea.location order by dea.date) as cumulVaccinations
from portfolioProject..CovidDeaths dea
join portfolioProject..CovidVaccinations vac
on dea.location=vac.location and dea.date=vac.date
where dea.continent is not null)
 
select country, population, max(cumulVacc) as totalvaccin, max(cumulVacc)/population*100 vaccPercentage
from popVac
group by country, population
order by country

-- total vaccination percentage vs population (using tem table)
drop table  if exists #popVaccin --avoiding table already existing error 
create table #popVaccin (country varchar(50) null, date datetime , population float, newVac float null, cumulVacc float null)
insert into #popVaccin 
select dea.location, dea.date, population , vac.new_vaccinations, sum(vac.new_vaccinations) over (partition by dea.location order by dea.date) as cumulVaccinations
from portfolioProject..CovidDeaths dea
join portfolioProject..CovidVaccinations vac
on dea.location=vac.location and dea.date=vac.date
where dea.continent is not null
-- using the temp table
select * from #popVaccin

select country, population, max(cumulVacc) as totalvaccin, max(cumulVacc)/population*100 vaccPercentage
from #popVaccin
group by country, population
order by country




