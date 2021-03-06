choice = input('Type 1 to convert from Roman numerals to Arabic numbers or type 2 to convert from Arabic numbers to Roman numerals: ')

if choice == '1':
    roman_numeral = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

    nums = list()
    result = 0


    def convertor(roman):
        for num in roman:
            nums.append(roman_numeral[num])

        i = 0
        while i < len(nums) - 1:
            if nums[i] < nums[i + 1]:
                nums[i] = nums[i] * -1
                i = i + 2
            else:
                i = i + 1

        result = 0
        for num in nums:
            result = result + num

        print('\nThe Roman numeral ' + roman + ' is equal to ' + str(result) + ' in Arabic.')


    roman = input('Enter a Roman numeral that you want to convert to Arabic numbers: ').upper().strip()
    convertor(roman)


elif choice == '2':
    roman_numeral = ["I", "IV", "V", "IX", "X", "XL", "L", "XC", "C", "CD", "D", "CM", "M"]
    arabic_numeral = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000]


    def converter(arabic):
        result = ''
        i = 12
        while arabic != 0:
            if arabic_numeral[i] <= arabic:
                result += roman_numeral[i]
                arabic -= arabic_numeral[i]
            else:
                i -= 1

        print('\nThe Roman numeral for ' + str(arabic1) + ' is ' + result)


    arabic = int(input('Enter an Arabic number that you want to convert to Roman numeral: ').strip())
    arabic1 = arabic
    converter(arabic)


else:
    print('Invalid input, Please choose 1 or 2.')
